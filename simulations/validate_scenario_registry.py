#!/usr/bin/env python3
"""Validate the Amendment 2 machine-readable scenario registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_MODELS = {"R0", "R1", "R2", "S0", "VOT", "R3", "R4", "R5", "R6"}
REQUIRED_GENERATORS = {"R1", "R2", "S0", "VOT", "R3", "R4", "R5", "R6"}
TRUTHS = {"FOLD", "NON_FOLD"}
REQUIRED_SCENARIO_FIELDS = {
    "id",
    "truth",
    "generator",
    "cases",
    "observations_per_arm",
    "arms",
    "action_stream",
    "control_coverage",
    "process_noise_sd",
    "measurement_noise_sd",
    "missingness_rate",
    "seed",
}


class RegistryError(ValueError):
    pass


def load_registry(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise RegistryError("registry root must be an object")
    return data


def validate_registry(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    models = data.get("models")
    if not isinstance(models, dict):
        errors.append("models must be an object")
        models = {}
    missing_models = REQUIRED_MODELS - set(models)
    if missing_models:
        errors.append(f"missing models: {', '.join(sorted(missing_models))}")

    common = data.get("common_contract")
    if not isinstance(common, dict):
        errors.append("common_contract must be an object")
        common = {}
    if common.get("action_stream_required_for_d5") is not True:
        errors.append("common contract must require an action stream for D5")
    if common.get("external_forcing_must_be_separate_from_action") is not True:
        errors.append("external forcing must be separate from agent action")

    scenarios = data.get("calibration_scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        errors.append("calibration_scenarios must be a non-empty array")
        scenarios = []

    ids: set[str] = set()
    generators: set[str] = set()
    truths: set[str] = set()
    for index, scenario in enumerate(scenarios):
        location = f"calibration_scenarios[{index}]"
        if not isinstance(scenario, dict):
            errors.append(f"{location} must be an object")
            continue
        missing = REQUIRED_SCENARIO_FIELDS - set(scenario)
        if missing:
            errors.append(f"{location} missing: {', '.join(sorted(missing))}")
            continue
        scenario_id = scenario["id"]
        if scenario_id in ids:
            errors.append(f"duplicate scenario id: {scenario_id}")
        ids.add(scenario_id)
        truth = scenario["truth"]
        if truth not in TRUTHS:
            errors.append(f"{location} has invalid truth: {truth}")
        truths.add(truth)
        generator = scenario["generator"]
        if generator not in models:
            errors.append(f"{location} uses unknown generator: {generator}")
        generators.add(generator)
        if scenario["cases"] <= 0 or scenario["observations_per_arm"] <= 0:
            errors.append(f"{location} cases and observations_per_arm must be positive")
        if scenario["arms"] != ["decline", "recovery"]:
            errors.append(f"{location} must contain ordered decline and recovery arms")
        if generator in {"VOT", "R3", "R4", "R5", "R6"} and scenario["action_stream"] != "observed":
            errors.append(f"{location} must observe actions for active-inference calibration")
        if generator in {"VOT", "R6"}:
            parameters = scenario.get("parameters")
            if not isinstance(parameters, dict):
                errors.append(f"{location} must declare fold parameters")
            else:
                for parameter in ("alpha", "beta", "zeta", "delta"):
                    value = parameters.get(parameter)
                    if not isinstance(value, (int, float)):
                        errors.append(f"{location} fold parameter {parameter} must be numeric")
                if isinstance(parameters.get("alpha"), (int, float)) and parameters["alpha"] <= 0:
                    errors.append(f"{location} fold parameter alpha must be positive")
                if isinstance(parameters.get("delta"), (int, float)) and parameters["delta"] <= 0:
                    errors.append(f"{location} fold parameter delta must be positive")
                if generator == "R6":
                    heterogeneity = parameters.get("hierogeneity_sd")
                    if not isinstance(heterogeneity, (int, float)) or heterogeneity <= 0:
                        errors.append(f"{location} R6 hierarchy requires positive heterogeneity_sd")
        for rate_field in ("missingness_rate",):
            value = scenario[rate_field]
            if not isinstance(value, (int, float)) or not 0 <= value < 1:
                errors.append(f"{location} {rate_field} must be in [0,1)")
        for positive_field in ("process_noise_sd", "measurement_noise_sd"):
            value = scenario[positive_field]
            if not isinstance(value, (int, float)) or value <= 0:
                errors.append(f"{location} {positive_field} must be positive")
        if not isinstance(scenario["seed"], int):
            errors.append(f"{location} seed must be an integer")

    missing_generators = REQUIRED_GENERATORS - generators
    if missing_generators:
        errors.append(f"calibration scenarios omit generators: {', '.join(sorted(missing_generators))}")
    if truths != TRUTHS:
        errors.append("calibration scenarios must contain both FOLD and NON_FOLD truth")

    targets = data.get("candidate_targets_not_ratified")
    if not isinstance(targets, dict):
        errors.append("candidate_targets_not_ratified must be an object")
        targets = {}
    if targets.get("meaningful_elpd_joint_margin", "missing") is not None:
        errors.append("meaningful margin must remain null until calibration and author ratification")

    locked = data.get("locked_validation_templates")
    if not isinstance(locked, list) or len(locked) < 2:
        errors.append("locked_validation_templates must contain both truth families")
        locked = []
    locked_truths = {item.get("truth") for item in locked if isinstance(item, dict)}
    if locked_truths != TRUTHS:
        errors.append("locked validation templates must contain FOLD and NON_FOLD")
    locked_ready = bool(locked) and all(
        isinstance(item, dict)
        and item.get("parameter_grid") != "UNSET_BEFORE_RATIFICATION"
        and item.get("seed_commitment") != "UNSET_BEFORE_RATIFICATION"
        for item in locked
    )

    if errors:
        raise RegistryError("; ".join(errors))

    return {
        "schema_version": data.get("schema_version"),
        "models_present": sorted(models),
        "scenario_count": len(scenarios),
        "truths_present": sorted(truths),
        "generators_present": sorted(generators),
        "locked_validation_ready": locked_ready,
        "registry_declares_ready": data.get("registry_ready_for_locked_validation") is True,
        "status": "VALID_DRAFT" if not locked_ready else "VALID_LOCKED_REGISTRY"
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("registry", type=Path)
    parser.add_argument("--require-locked", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        report = validate_registry(load_registry(args.registry))
    except (OSError, json.JSONDecodeError, RegistryError) as exc:
        raise SystemExit(f"registry error: {exc}") from exc
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.require_locked and not report["locked_validation_ready"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
