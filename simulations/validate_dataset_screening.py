#!/usr/bin/env python3
"""Validate the Amendment 2 dataset census and candidate screening record."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


FACT_FIELDS = {
    "same_person_decline_recovery",
    "minimum_50_each_arm",
    "observed_state",
    "agent_action",
    "external_forcing",
    "action_forcing_distinct",
    "bidirectional_forcing",
    "independent_p3",
}
FACT_VALUES = {"yes", "no", "unknown"}
ALLOWED_STATUSES = {
    "BLOCKED_D4",
    "UNRESOLVED_METADATA",
    "BLOCKED_ACCESS",
    "READY_FOR_BLINDED_PREFLIGHT",
}
KNOWN_EXTERNAL_ROUTES = {
    "transid_tapering",
    "transid_recovery",
    "bipolar_early_warning",
}


class ScreeningError(ValueError):
    pass


def load_screening(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ScreeningError("screening root must be an object")
    return data


def validate_screening(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    census = data.get("catalogue_census")
    if not isinstance(census, dict):
        errors.append("catalogue_census must be an object")
        census = {}

    record_ids = census.get("record_ids")
    if not isinstance(record_ids, list) or not record_ids:
        errors.append("catalogue_census.record_ids must be a non-empty array")
        record_ids = []
    if len(record_ids) != len(set(record_ids)):
        errors.append("catalogue record IDs must be unique")
    declared_count = census.get("declared_record_count")
    if declared_count != len(record_ids):
        errors.append(
            f"declared catalogue count {declared_count!r} does not match "
            f"enumerated count {len(record_ids)}"
        )
    if census.get("snapshot_commit") in {None, "", "UNSET"}:
        errors.append("catalogue snapshot commit must be fixed")
    if census.get("shortlist_regex") in {None, "", "UNSET"}:
        errors.append("shortlist regex must be recorded")

    shortlist_ids = census.get("shortlist_ids")
    if not isinstance(shortlist_ids, list):
        errors.append("catalogue_census.shortlist_ids must be an array")
        shortlist_ids = []
    if len(shortlist_ids) != len(set(shortlist_ids)):
        errors.append("shortlist IDs must be unique")
    if not set(shortlist_ids).issubset(set(record_ids)):
        errors.append("every shortlist ID must occur in the catalogue census")
    expected_non_shortlisted = len(record_ids) - len(shortlist_ids)
    if census.get("non_shortlisted_count") != expected_non_shortlisted:
        errors.append("non_shortlisted_count does not match census minus shortlist")
    if census.get("non_shortlisted_disposition") != "NOT_SHORTLISTED_METADATA":
        errors.append("non-shortlisted records must use NOT_SHORTLISTED_METADATA")

    external_routes = data.get("known_external_routes")
    if not isinstance(external_routes, list):
        errors.append("known_external_routes must be an array")
        external_routes = []
    if set(external_routes) != KNOWN_EXTERNAL_ROUTES:
        errors.append("known external routes are incomplete or unexpected")

    candidates = data.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        errors.append("candidates must be a non-empty array")
        candidates = []

    candidate_ids: set[str] = set()
    reviewed_catalogue_ids: set[str] = set()
    ready_count = 0
    for index, candidate in enumerate(candidates):
        location = f"candidates[{index}]"
        if not isinstance(candidate, dict):
            errors.append(f"{location} must be an object")
            continue
        candidate_id = candidate.get("candidate_id")
        if not isinstance(candidate_id, str) or not candidate_id:
            errors.append(f"{location}.candidate_id must be a non-empty string")
        elif candidate_id in candidate_ids:
            errors.append(f"duplicate candidate ID: {candidate_id}")
        else:
            candidate_ids.add(candidate_id)

        catalogue_id = candidate.get("catalogue_record_id")
        if catalogue_id is not None:
            if catalogue_id not in record_ids:
                errors.append(f"{location} references an unknown catalogue record")
            reviewed_catalogue_ids.add(catalogue_id)

        urls = candidate.get("evidence_urls")
        if (
            not isinstance(urls, list)
            or not urls
            or any(not isinstance(url, str) or not url.startswith("https://") for url in urls)
        ):
            errors.append(f"{location}.evidence_urls must contain HTTPS URLs")

        status = candidate.get("status")
        if status == "RUNNABLE":
            errors.append(f"{location} may not be labelled RUNNABLE by screening")
        if status not in ALLOWED_STATUSES:
            errors.append(f"{location} has invalid status: {status!r}")
        if status == "READY_FOR_BLINDED_PREFLIGHT":
            ready_count += 1

        facts = candidate.get("facts")
        if not isinstance(facts, dict):
            errors.append(f"{location}.facts must be an object")
            facts = {}
        missing_facts = FACT_FIELDS - set(facts)
        extra_facts = set(facts) - FACT_FIELDS
        if missing_facts:
            errors.append(f"{location} missing facts: {', '.join(sorted(missing_facts))}")
        if extra_facts:
            errors.append(f"{location} has unknown facts: {', '.join(sorted(extra_facts))}")
        for fact_name, value in facts.items():
            if value not in FACT_VALUES:
                errors.append(f"{location}.{fact_name} has invalid value: {value!r}")

        if status == "BLOCKED_D4" and not (
            facts.get("same_person_decline_recovery") == "no"
            or facts.get("minimum_50_each_arm") == "no"
        ):
            errors.append(f"{location} is BLOCKED_D4 without an explicit D4 failure")
        if status == "BLOCKED_ACCESS" and candidate.get("access") == "open":
            errors.append(f"{location} is BLOCKED_ACCESS but declares open access")
        if status == "READY_FOR_BLINDED_PREFLIGHT":
            hard_fields = FACT_FIELDS - {"independent_p3"}
            not_yes = sorted(name for name in hard_fields if facts.get(name) != "yes")
            if not_yes:
                errors.append(
                    f"{location} is ready but necessary facts are not yes: "
                    f"{', '.join(not_yes)}"
                )
        if not candidate.get("rationale"):
            errors.append(f"{location}.rationale must be recorded")

    if reviewed_catalogue_ids != set(shortlist_ids):
        missing = sorted(set(shortlist_ids) - reviewed_catalogue_ids)
        extra = sorted(reviewed_catalogue_ids - set(shortlist_ids))
        errors.append(
            "manual catalogue review must equal the automated shortlist "
            f"(missing={missing}, extra={extra})"
        )
    missing_external_candidates = KNOWN_EXTERNAL_ROUTES - candidate_ids
    if missing_external_candidates:
        errors.append(
            "missing external candidate records: "
            + ", ".join(sorted(missing_external_candidates))
        )

    expected_status = (
        "BOUNDED_SEARCH_COMPLETE_PREFLIGHT_CANDIDATE_IDENTIFIED"
        if ready_count
        else "BOUNDED_SEARCH_COMPLETE_NO_ELIGIBLE_TARGET_IDENTIFIED"
    )
    if data.get("status") != expected_status:
        errors.append(f"root status must be {expected_status}")
    conclusion = data.get("conclusion", "")
    if not isinstance(conclusion, str) or "not a claim of universal absence" not in conclusion.lower():
        errors.append("conclusion must explicitly reject a universal-absence claim")

    if errors:
        raise ScreeningError("; ".join(errors))

    return {
        "schema_version": data.get("schema_version"),
        "catalogue_record_count": len(record_ids),
        "shortlist_count": len(shortlist_ids),
        "external_route_count": len(external_routes),
        "candidate_count": len(candidates),
        "ready_for_blinded_preflight_count": ready_count,
        "status": expected_status,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("registry", type=Path)
    parser.add_argument(
        "--require-target",
        action="store_true",
        help="exit 2 unless at least one target is ready for blinded preflight",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        report = validate_screening(load_screening(args.registry))
    except (OSError, json.JSONDecodeError, ScreeningError) as exc:
        raise SystemExit(f"screening error: {exc}") from exc
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.require_target and report["ready_for_blinded_preflight_count"] == 0:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
