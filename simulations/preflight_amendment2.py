#!/usr/bin/env python3
"""Check hard necessary conditions for an Amendment 2 target dataset."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


UNSET = {None, "", "UNSET"}
ACTION_STATUSES = {"observed", "proxy", "absent", "UNSET"}
FORCING_STATUSES = {"observed", "absent", "UNSET"}
ENDPOINT_STATUSES = {"observed", "absent", "UNSET"}


class ManifestError(ValueError):
    pass


def load_manifest(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ManifestError("manifest root must be an object")
    return data


def _object(parent: dict[str, Any], key: str) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        raise ManifestError(f"{key} must be an object")
    return value


def _is_unset(value: Any) -> bool:
    try:
        return value in UNSET
    except TypeError:
        return False


def evaluate_manifest(data: dict[str, Any]) -> dict[str, Any]:
    prospective = _object(data, "prospective_status")
    design = _object(data, "design")
    variables = _object(data, "variables")
    observed_state = _object(variables, "observed_state")
    action = _object(variables, "agent_action")
    forcing = _object(variables, "external_forcing")
    endpoint = _object(variables, "endpoint")
    separation = _object(data, "separation")
    parameterization = _object(data, "parameterization")

    blockers: list[dict[str, str]] = []
    unspecified: list[str] = []

    def block(code: str, scope: str, message: str) -> None:
        blockers.append({"code": code, "scope": scope, "message": message})

    def require_text(value: Any, path: str) -> None:
        if _is_unset(value):
            unspecified.append(path)
        elif not isinstance(value, str):
            raise ManifestError(f"{path} must be a string")

    require_text(data.get("dataset_id"), "dataset_id")
    require_text(data.get("schema_version"), "schema_version")
    require_text(design.get("time_unit"), "design.time_unit")
    require_text(design.get("missing_data_rule"), "design.missing_data_rule")
    require_text(design.get("irregular_timing_rule"), "design.irregular_timing_rule")

    inspected = prospective.get("target_outcomes_inspected_before_freeze")
    if not isinstance(inspected, bool):
        raise ManifestError("prospective_status.target_outcomes_inspected_before_freeze must be boolean")
    if inspected:
        block(
            "TARGET_OUTCOME_ALREADY_INSPECTED",
            "RATIFICATION",
            "this target cannot supply a prospective Amendment 2 ratification",
        )

    mapping_frozen = prospective.get("variable_mapping_frozen")
    if not isinstance(mapping_frozen, bool):
        raise ManifestError("prospective_status.variable_mapping_frozen must be boolean")
    if not mapping_frozen:
        unspecified.append("prospective_status.variable_mapping_frozen")

    cases = design.get("cases")
    if cases is None:
        unspecified.append("design.cases")
    elif not isinstance(cases, int) or isinstance(cases, bool) or cases <= 0:
        raise ManifestError("design.cases must be a positive integer or null")

    arms = design.get("arms")
    if arms != ["decline", "recovery"]:
        block("MISSING_PAIRED_ARMS", "BOTH", "ordered decline and recovery arms are required")

    observations = _object(design, "observations_per_arm")
    for arm in ("decline", "recovery"):
        value = observations.get(arm)
        if value is None:
            unspecified.append(f"design.observations_per_arm.{arm}")
        elif not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ManifestError(f"design.observations_per_arm.{arm} must be a positive integer or null")

    state_names = observed_state.get("names")
    if not isinstance(state_names, list) or not all(isinstance(item, str) for item in state_names):
        raise ManifestError("variables.observed_state.names must be an array of strings")
    if not state_names:
        unspecified.append("variables.observed_state.names")
    require_text(observed_state.get("mapping"), "variables.observed_state.mapping")

    action_status = action.get("status")
    if action_status not in ACTION_STATUSES:
        raise ManifestError(f"variables.agent_action.status must be one of {sorted(ACTION_STATUSES)}")
    if action_status == "UNSET":
        unspecified.append("variables.agent_action.status")
    elif action_status == "absent":
        block("ACTION_STREAM_ABSENT", "D5", "active-inference policy selection is not adjudicable")
    else:
        require_text(action.get("name"), "variables.agent_action.name")
        justified = action.get("prospectively_justified")
        if not isinstance(justified, bool):
            raise ManifestError("variables.agent_action.prospectively_justified must be boolean")
        if not justified:
            block("ACTION_MAPPING_NOT_JUSTIFIED", "D5", "action or proxy mapping must be justified prospectively")
        if action_status == "proxy":
            require_text(action.get("proxy_justification"), "variables.agent_action.proxy_justification")

    forcing_status = forcing.get("status")
    if forcing_status not in FORCING_STATUSES:
        raise ManifestError(f"variables.external_forcing.status must be one of {sorted(FORCING_STATUSES)}")
    if forcing_status == "UNSET":
        unspecified.append("variables.external_forcing.status")
    elif forcing_status == "absent":
        block("EXTERNAL_FORCING_ABSENT", "STRUCTURE", "two-sided fold traversal is not adjudicable")
    else:
        require_text(forcing.get("name"), "variables.external_forcing.name")
        for field, code, message in (
            ("exogenous", "FORCING_NOT_EXOGENOUS", "external forcing is not declared exogenous"),
            ("bidirectional", "FORCING_NOT_BIDIRECTIONAL", "decline and recovery traversal is not bidirectional"),
        ):
            value = forcing.get(field)
            if not isinstance(value, bool):
                raise ManifestError(f"variables.external_forcing.{field} must be boolean")
            if not value:
                block(code, "STRUCTURE", message)
        require_text(forcing.get("coverage"), "variables.external_forcing.coverage")

    distinct = separation.get("action_distinct_from_external_forcing")
    if not isinstance(distinct, bool):
        raise ManifestError("separation.action_distinct_from_external_forcing must be boolean")
    if action_status in {"observed", "proxy"} and forcing_status == "observed":
        same_name = action.get("name") == forcing.get("name") and not _is_unset(action.get("name"))
        if not distinct or same_name:
            block(
                "ACTION_FORCING_CONFLATED",
                "BOTH",
                "agent action and external forcing must be different recorded variables",
            )

    endpoint_status = endpoint.get("status")
    if endpoint_status not in ENDPOINT_STATUSES:
        raise ManifestError(f"variables.endpoint.status must be one of {sorted(ENDPOINT_STATUSES)}")
    if endpoint_status == "UNSET":
        unspecified.append("variables.endpoint.status")
    elif endpoint_status == "absent":
        block("ENDPOINT_ABSENT", "P3", "P3 and endpoint-scored comparisons cannot be run")
    else:
        require_text(endpoint.get("name"), "variables.endpoint.name")

    for field in (
        "latent_state_dimension_grid",
        "action_set",
        "policy_horizon_grid",
        "prior_sensitivity_grid",
    ):
        value = parameterization.get(field)
        if _is_unset(value) or value == [] or value == {}:
            unspecified.append(f"parameterization.{field}")

    if blockers:
        status = "HARD_BLOCKED"
    elif unspecified:
        status = "INCOMPLETE"
    else:
        status = "NECESSARY_CONDITIONS_MET_NOT_SUFFICIENT"

    return {
        "schema_version": data.get("schema_version"),
        "dataset_id": data.get("dataset_id"),
        "status": status,
        "necessary_conditions_met": status == "NECESSARY_CONDITIONS_MET_NOT_SUFFICIENT",
        "runnable_claimed": False,
        "blockers": blockers,
        "unspecified": sorted(set(unspecified)),
        "caveat": "preflight checks necessary conditions only; simulation must establish sufficiency",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument(
        "--require-necessary-conditions",
        action="store_true",
        help="exit 2 unless the manifest clears all hard and incomplete preflight checks",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        report = evaluate_manifest(load_manifest(args.manifest))
    except (OSError, json.JSONDecodeError, ManifestError) as exc:
        raise SystemExit(f"preflight error: {exc}") from exc
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.require_necessary_conditions and not report["necessary_conditions_met"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
