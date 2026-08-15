#!/usr/bin/env python3
"""Reproduce the openESM census and shortlist from a fixed local checkout."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Iterable

try:
    from simulations.validate_dataset_screening import load_screening, validate_screening
except ModuleNotFoundError:  # direct script execution from simulations/
    from validate_dataset_screening import load_screening, validate_screening


class ReproductionError(ValueError):
    pass


def metadata_text(metadata: dict[str, Any]) -> str:
    parts = [
        metadata.get("additional_comments"),
        metadata.get("topics"),
        metadata.get("participants"),
    ]
    features = metadata.get("features") or []
    for feature in features:
        if not isinstance(feature, dict):
            continue
        parts.extend(
            feature.get(field)
            for field in ("name", "description", "construct", "coding", "comments")
        )
    return " ".join(str(part) for part in parts if part is not None)


def screen_metadata_files(
    paths: Iterable[Path], pattern: str
) -> tuple[list[str], list[str]]:
    expression = re.compile(pattern, re.IGNORECASE)
    record_ids: list[str] = []
    shortlist_ids: list[str] = []
    for path in sorted(paths):
        with path.open("r", encoding="utf-8") as handle:
            metadata = json.load(handle)
        record_id = str(metadata.get("dataset_id", ""))
        if not re.fullmatch(r"\d{4}", record_id):
            raise ReproductionError(f"{path}: missing or invalid four-digit dataset_id")
        record_ids.append(record_id)
        if expression.search(metadata_text(metadata)):
            shortlist_ids.append(record_id)
    if len(record_ids) != len(set(record_ids)):
        raise ReproductionError("duplicate dataset_id in catalogue checkout")
    return sorted(record_ids), sorted(shortlist_ids)


def checkout_commit(catalogue_root: Path) -> str:
    try:
        result = subprocess.run(
            [
                "git",
                "-c",
                f"safe.directory={catalogue_root.resolve()}",
                "-C",
                str(catalogue_root),
                "rev-parse",
                "HEAD",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        raise ReproductionError(f"cannot execute git for catalogue checkout: {exc}") from exc
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or str(exc)).strip()
        raise ReproductionError(f"cannot read catalogue checkout commit: {detail}") from exc
    return result.stdout.strip()


def reproduce(catalogue_root: Path, registry: dict[str, Any]) -> dict[str, Any]:
    validate_screening(registry)
    census = registry["catalogue_census"]
    actual_commit = checkout_commit(catalogue_root)
    expected_commit = census["snapshot_commit"]
    if actual_commit != expected_commit:
        raise ReproductionError(
            f"catalogue commit mismatch: expected {expected_commit}, got {actual_commit}"
        )

    paths = list((catalogue_root / "datasets").glob("**/*_metadata.json"))
    actual_ids, actual_shortlist = screen_metadata_files(paths, census["shortlist_regex"])
    expected_ids = sorted(census["record_ids"])
    expected_shortlist = sorted(census["shortlist_ids"])
    if actual_ids != expected_ids:
        raise ReproductionError(
            f"catalogue enumeration differs: expected {len(expected_ids)} IDs, "
            f"got {len(actual_ids)}"
        )
    if actual_shortlist != expected_shortlist:
        raise ReproductionError(
            "shortlist differs: "
            f"expected {expected_shortlist}, got {actual_shortlist}"
        )
    return {
        "snapshot_commit": actual_commit,
        "catalogue_record_count": len(actual_ids),
        "shortlist_count": len(actual_shortlist),
        "shortlist_ids": actual_shortlist,
        "status": "REPRODUCED",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalogue_root", type=Path)
    parser.add_argument("registry", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        report = reproduce(args.catalogue_root, load_screening(args.registry))
    except (OSError, json.JSONDecodeError, ReproductionError, ValueError) as exc:
        raise SystemExit(f"reproduction error: {exc}") from exc
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
