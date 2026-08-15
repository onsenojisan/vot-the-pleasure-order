#!/usr/bin/env python3
"""Summarize two-sided Amendment 2 simulation outcomes.

This program deliberately does not implement a fold or active-inference model.
It enforces the result-file and worst-case acceptance contract after the
generative and fitting models have been frozen elsewhere.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Iterable


TRUTHS = {"FOLD", "NON_FOLD"}
DISPOSITIONS = {"FOLD", "NO_FOLD", "TIE", "UNDERPOWERED", "UNIDENTIFIED"}
REQUIRED_FIELDS = {"scenario_id", "truth", "replicate", "disposition"}


def wilson_interval(successes: int, total: int, z: float = 1.959963984540054) -> tuple[float, float]:
    """Return a two-sided Wilson score interval for a binomial proportion."""
    if total <= 0:
        raise ValueError("total must be positive")
    if successes < 0 or successes > total:
        raise ValueError("successes must be between zero and total")
    p = successes / total
    z2 = z * z
    denominator = 1.0 + z2 / total
    center = (p + z2 / (2.0 * total)) / denominator
    radius = z * math.sqrt((p * (1.0 - p) + z2 / (4.0 * total)) / total) / denominator
    return max(0.0, center - radius), min(1.0, center + radius)


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        missing = REQUIRED_FIELDS - fields
        if missing:
            raise ValueError(f"missing required columns: {', '.join(sorted(missing))}")
        rows = list(reader)

    if not rows:
        raise ValueError("result file contains no rows")

    seen: set[tuple[str, str]] = set()
    scenario_truth: dict[str, str] = {}
    for line_number, row in enumerate(rows, start=2):
        scenario = row["scenario_id"].strip()
        truth = row["truth"].strip().upper()
        replicate = row["replicate"].strip()
        disposition = row["disposition"].strip().upper()
        if not scenario or not replicate:
            raise ValueError(f"line {line_number}: scenario_id and replicate are required")
        if truth not in TRUTHS:
            raise ValueError(f"line {line_number}: invalid truth {truth!r}")
        if disposition not in DISPOSITIONS:
            raise ValueError(f"line {line_number}: invalid disposition {disposition!r}")
        key = (scenario, replicate)
        if key in seen:
            raise ValueError(f"line {line_number}: duplicate scenario/replicate {key}")
        seen.add(key)
        previous = scenario_truth.setdefault(scenario, truth)
        if previous != truth:
            raise ValueError(f"line {line_number}: scenario {scenario!r} has mixed truths")
        row["scenario_id"] = scenario
        row["truth"] = truth
        row["replicate"] = replicate
        row["disposition"] = disposition
    return rows


def _metric(successes: int, total: int) -> dict[str, float | int]:
    lower, upper = wilson_interval(successes, total)
    return {
        "count": successes,
        "rate": successes / total,
        "wilson_95_lower": lower,
        "wilson_95_upper": upper,
    }


def summarize(
    rows: Iterable[dict[str, str]],
    power_floor: float = 0.80,
    false_error_ceiling: float = 0.05,
    mcse_ceiling: float = 0.01,
) -> dict[str, object]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["scenario_id"]].append(row)
    if not grouped:
        raise ValueError("no scenarios to summarize")

    reports: list[dict[str, object]] = []
    truths_present: set[str] = set()
    for scenario in sorted(grouped):
        scenario_rows = grouped[scenario]
        truth = scenario_rows[0]["truth"]
        truths_present.add(truth)
        total = len(scenario_rows)
        correct_label = "FOLD" if truth == "FOLD" else "NO_FOLD"
        opposite_label = "NO_FOLD" if truth == "FOLD" else "FOLD"
        correct = sum(row["disposition"] == correct_label for row in scenario_rows)
        opposite = sum(row["disposition"] == opposite_label for row in scenario_rows)
        inconclusive = total - correct - opposite
        correct_metric = _metric(correct, total)
        opposite_metric = _metric(opposite, total)
        inconclusive_metric = _metric(inconclusive, total)
        worst_case_mcse = 0.5 / math.sqrt(total)
        passes = (
            correct_metric["wilson_95_lower"] >= power_floor
            and opposite_metric["wilson_95_upper"] <= false_error_ceiling
            and worst_case_mcse <= mcse_ceiling
        )
        reports.append(
            {
                "scenario_id": scenario,
                "truth": truth,
                "replicates": total,
                "correct_disposition": correct_label,
                "correct": correct_metric,
                "opposite_error_disposition": opposite_label,
                "opposite_error": opposite_metric,
                "inconclusive": inconclusive_metric,
                "worst_case_mcse": worst_case_mcse,
                "passes_targets": passes,
            }
        )

    both_truths = truths_present == TRUTHS
    all_scenarios_pass = all(bool(report["passes_targets"]) for report in reports)
    return {
        "contract_version": "2026-08-15",
        "targets": {
            "power_lower_95_floor": power_floor,
            "opposite_error_upper_95_ceiling": false_error_ceiling,
            "worst_case_mcse_ceiling": mcse_ceiling,
        },
        "truth_families_present": sorted(truths_present),
        "both_truth_families_present": both_truths,
        "all_scenarios_pass": all_scenarios_pass,
        "overall_pass": both_truths and all_scenarios_pass,
        "scenarios": reports,
    }


def _probability(value: str) -> float:
    parsed = float(value)
    if not 0.0 <= parsed <= 1.0:
        raise argparse.ArgumentTypeError("must be between 0 and 1")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path, help="UTF-8 CSV with one row per simulation replicate")
    parser.add_argument("--output", type=Path, help="write the JSON report to this path")
    parser.add_argument("--power-floor", type=_probability, default=0.80)
    parser.add_argument("--false-error-ceiling", type=_probability, default=0.05)
    parser.add_argument("--mcse-ceiling", type=_probability, default=0.01)
    parser.add_argument(
        "--require-pass",
        action="store_true",
        help="exit with status 2 unless every scenario and both truth families pass",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        report = summarize(
            load_rows(args.results),
            power_floor=args.power_floor,
            false_error_ceiling=args.false_error_ceiling,
            mcse_ceiling=args.mcse_ceiling,
        )
    except (OSError, ValueError) as exc:
        raise SystemExit(f"calibration error: {exc}") from exc

    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    if args.require_pass and not report["overall_pass"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
