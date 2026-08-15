import copy
import unittest
from pathlib import Path

from simulations.validate_dataset_screening import (
    ScreeningError,
    load_screening,
    validate_screening,
)


REGISTRY = Path(__file__).with_name("amendment2_dataset_screening.v0.json")


class DatasetScreeningValidationTests(unittest.TestCase):
    def test_current_registry_is_valid_and_has_no_preflight_target(self):
        report = validate_screening(load_screening(REGISTRY))
        self.assertEqual(report["catalogue_record_count"], 62)
        self.assertEqual(report["shortlist_count"], 11)
        self.assertEqual(report["additional_catalogue_search_count"], 1)
        self.assertEqual(report["additional_catalogue_record_count"], 5)
        self.assertEqual(report["candidate_count"], 18)
        self.assertEqual(report["target_blind_review_count"], 6)
        self.assertEqual(report["ready_for_blinded_preflight_count"], 0)

    def test_declared_count_must_match_enumeration(self):
        broken = copy.deepcopy(load_screening(REGISTRY))
        broken["catalogue_census"]["declared_record_count"] = 63
        with self.assertRaises(ScreeningError):
            validate_screening(broken)

    def test_every_shortlisted_record_requires_manual_disposition(self):
        broken = copy.deepcopy(load_screening(REGISTRY))
        broken["candidates"] = [
            candidate
            for candidate in broken["candidates"]
            if candidate.get("catalogue_record_id") != "0014"
        ]
        with self.assertRaises(ScreeningError):
            validate_screening(broken)

    def test_additional_query_union_and_dispositions_must_match(self):
        broken = copy.deepcopy(load_screening(REGISTRY))
        broken["additional_catalogue_searches"][0]["union_record_ids"].pop()
        with self.assertRaises(ScreeningError):
            validate_screening(broken)

    def test_same_study_records_must_map_to_the_declared_candidate(self):
        broken = copy.deepcopy(load_screening(REGISTRY))
        candidate = next(
            item
            for item in broken["candidates"]
            if item["candidate_id"] == "zenodo_lifetrace"
        )
        candidate["source_record_ids"] = ["17249917"]
        with self.assertRaises(ScreeningError):
            validate_screening(broken)

    def test_screening_cannot_label_a_dataset_runnable(self):
        broken = copy.deepcopy(load_screening(REGISTRY))
        broken["candidates"][0]["status"] = "RUNNABLE"
        with self.assertRaises(ScreeningError):
            validate_screening(broken)

    def test_blocked_d4_requires_an_explicit_failed_fact(self):
        broken = copy.deepcopy(load_screening(REGISTRY))
        candidate = broken["candidates"][0]
        candidate["facts"]["same_person_decline_recovery"] = "unknown"
        candidate["facts"]["minimum_50_each_arm"] = "unknown"
        with self.assertRaises(ScreeningError):
            validate_screening(broken)

    def test_ready_status_requires_all_non_p3_facts(self):
        broken = copy.deepcopy(load_screening(REGISTRY))
        candidate = broken["candidates"][1]
        candidate["status"] = "READY_FOR_BLINDED_PREFLIGHT"
        broken["status"] = "BOUNDED_SEARCH_COMPLETE_PREFLIGHT_CANDIDATE_IDENTIFIED"
        with self.assertRaises(ScreeningError):
            validate_screening(broken)

    def test_target_blind_review_cannot_inspect_participant_level_outcome_values(self):
        broken = copy.deepcopy(load_screening(REGISTRY))
        candidate = next(
            item
            for item in broken["candidates"]
            if item["candidate_id"] == "openesm_0014_habets"
        )
        candidate["target_blind_review"][
            "participant_level_outcome_values_inspected"
        ] = True
        with self.assertRaises(ScreeningError):
            validate_screening(broken)

    def test_target_blind_review_cannot_use_published_results_for_disposition(self):
        broken = copy.deepcopy(load_screening(REGISTRY))
        candidate = next(
            item
            for item in broken["candidates"]
            if item["candidate_id"] == "openesm_0060_beck"
        )
        candidate["target_blind_review"][
            "published_aggregate_results_used_for_disposition"
        ] = True
        with self.assertRaises(ScreeningError):
            validate_screening(broken)


if __name__ == "__main__":
    unittest.main()
