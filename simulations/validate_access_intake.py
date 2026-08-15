#!/usr/bin/env python3
"""Validate a metadata-only Amendment 2 controlled-access intake."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


TRI_VALUES = {"yes", "no", "unknown"}
ACCESS_ROUTES = {
    "controlled_local_execution",
    "controlled_transfer",
    "unavailable",
    "unknown",
}
INSTITUTIONAL_STATUSES = {"confirmed", "not_confirmed", "not_required", "unknown"}
UNSET = {None, "", "UNSET"}


class IntakeError(ValueError):
    pass


def load_intake(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise IntakeError("intake root must be an object")
    return data


def _object(parent: dict[str, Any], key: str) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        raise IntakeError(f"{key} must be an object")
    return value


def _require_tri(parent: dict[str, Any], key: str, path: str) -> str:
    value = parent.get(key)
    if value not in TRI_VALUES:
        raise IntakeError(f"{path}.{key} must be one of {sorted(TRI_VALUES)}")
    return value


def evaluate_intake(data: dict[str, Any]) -> dict[str, Any]:
    safeguards = _object(data, "safeguards")
    design = _object(data, "design")
    arm_labels = _object(design, "arm_labels")
    observations = _object(design, "observations_per_person")
    variables = _object(data, "variables")
    access = _object(data, "access")

    incomplete: list[str] = []
    safety_reasons: list[str] = []
    for field in ("schema_version", "candidate_id", "review_date", "completed_by_role"):
        if data.get(field) in UNSET:
            incomplete.append(field)
        elif not isinstance(data.get(field), str):
            raise IntakeError(f"{field} must be a string")

    urls = data.get("evidence_urls")
    if not isinstance(urls, list) or any(
        not isinstance(url, str) or not url.startswith("https://") for url in urls
    ):
        raise IntakeError("evidence_urls must be an array of HTTPS URLs")
    if not urls:
        incomplete.append("evidence_urls")

    for field in (
        "participant_level_data_transferred_to_vot_team",
        "participant_level_outcome_values_inspected_by_vot_team",
        "published_aggregate_results_used_for_eligibility",
    ):
        value = safeguards.get(field)
        if not isinstance(value, bool):
            raise IntakeError(f"safeguards.{field} must be boolean")
        if value:
            safety_reasons.append(field)

    same_people = _require_tri(design, "same_people_in_decline_and_recovery", "design")
    for arm in ("decline", "recovery"):
        label = arm_labels.get(arm)
        if label in UNSET:
            incomplete.append(f"design.arm_labels.{arm}")
        elif not isinstance(label, str):
            raise IntakeError(f"design.arm_labels.{arm} must be a string")
        count = observations.get(arm)
        if count is None:
            incomplete.append(f"design.observations_per_person.{arm}")
        elif not isinstance(count, int) or isinstance(count, bool) or count <= 0:
            raise IntakeError(
                f"design.observations_per_person.{arm} must be a positive integer or null"
            )
    for field in ("time_unit", "arm_boundary_source"):
        if design.get(field) in UNSET:
            incomplete.append(f"design.{field}")
        elif not isinstance(design.get(field), str):
            raise IntakeError(f"design.{field} must be a string")

    if same_people == "no" or any(
        isinstance(observations.get(arm), int) and observations[arm] < 50
        for arm in ("decline", "recovery")
    ):
        d4_status = "FAILED"
    elif same_people == "unknown" or any(
        path.startswith("design.") for path in incomplete
    ):
        d4_status = "UNKNOWN"
    else:
        d4_status = "PASSES_METADATA_ONLY"

    variable_values = {
        field: _require_tri(variables, field, "variables")
        for field in (
            "observed_state",
            "agent_action_or_proxy",
            "external_forcing",
            "action_forcing_distinct",
            "bidirectional_forcing",
            "independent_non_self_report_endpoint",
        )
    }
    structural_fields = (
        "observed_state",
        "agent_action_or_proxy",
        "external_forcing",
        "action_forcing_distinct",
        "bidirectional_forcing",
    )
    if d4_status == "FAILED" or any(variable_values[field] == "no" for field in structural_fields):
        amendment2_mapping_status = "BLOCKED"
    elif d4_status != "PASSES_METADATA_ONLY" or any(
        variable_values[field] == "unknown" for field in structural_fields
    ):
        amendment2_mapping_status = "UNKNOWN"
    else:
        amendment2_mapping_status = "POTENTIALLY_MAPPABLE"

    route = access.get("route")
    if route not in ACCESS_ROUTES:
        raise IntakeError(f"access.route must be one of {sorted(ACCESS_ROUTES)}")
    requirement_values = {
        field: _require_tri(access, field, "access")
        for field in (
            "institutional_sponsor_required",
            "ethics_approval_required",
            "data_use_agreement_required",
            "local_offline_execution_possible",
        )
    }
    institutional_status = access.get("institutional_route_status")
    if institutional_status not in INSTITUTIONAL_STATUSES:
        raise IntakeError(
            "access.institutional_route_status must be one of "
            f"{sorted(INSTITUTIONAL_STATUSES)}"
        )
    if access.get("contact_route") in UNSET:
        incomplete.append("access.contact_route")
    elif not isinstance(access.get("contact_route"), str):
        raise IntakeError("access.contact_route must be a string")

    requires_institution = (
        requirement_values["institutional_sponsor_required"] == "yes"
        or requirement_values["ethics_approval_required"] == "yes"
    )
    if route == "unavailable" or (
        route == "controlled_local_execution"
        and requirement_values["local_offline_execution_possible"] == "no"
    ):
        access_status = "BLOCKED"
    elif (
        route == "unknown"
        or institutional_status == "unknown"
        or any(value == "unknown" for value in requirement_values.values())
    ):
        access_status = "UNKNOWN"
    elif requires_institution and institutional_status != "confirmed":
        access_status = "GOVERNANCE_REQUIRED"
    elif not requires_institution and institutional_status == "not_confirmed":
        access_status = "UNKNOWN"
    else:
        access_status = "POSSIBLE_NOT_APPROVED"

    if safety_reasons:
        status = "SAFETY_STOP"
    elif d4_status == "FAILED":
        status = "DESIGN_INELIGIBLE"
    elif d4_status == "UNKNOWN":
        status = "METADATA_INCOMPLETE"
    elif access_status == "BLOCKED":
        status = "ACCESS_BLOCKED"
    elif access_status == "UNKNOWN" or incomplete:
        status = "METADATA_INCOMPLETE"
    elif access_status == "GOVERNANCE_REQUIRED":
        status = "GOVERNANCE_REQUIRED"
    else:
        status = "ELIGIBLE_FOR_FORMAL_GOVERNANCE_REVIEW"

    return {
        "schema_version": data.get("schema_version"),
        "candidate_id": data.get("candidate_id"),
        "status": status,
        "d4_design_status": d4_status,
        "amendment2_mapping_status": amendment2_mapping_status,
        "p3_metadata_status": variable_values["independent_non_self_report_endpoint"],
        "access_status": access_status,
        "participant_data_access_authorized": False,
        "amendment2_verdict": "NO AMENDMENT 2 VERDICT",
        "safety_reasons": safety_reasons,
        "incomplete": sorted(set(incomplete)),
        "caveat": "metadata eligibility never authorizes data access, analysis or an Amendment 2 verdict",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("intake", type=Path)
    parser.add_argument(
        "--require-formal-review-eligibility",
        action="store_true",
        help="exit 2 unless metadata clears the gate for formal governance review",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        report = evaluate_intake(load_intake(args.intake))
    except (OSError, json.JSONDecodeError, IntakeError) as exc:
        raise SystemExit(f"access-intake error: {exc}") from exc
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if (
        args.require_formal_review_eligibility
        and report["status"] != "ELIGIBLE_FOR_FORMAL_GOVERNANCE_REVIEW"
    ):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
