import copy
import unittest
from pathlib import Path

from simulations.validate_access_intake import evaluate_intake, load_intake


TEMPLATE = Path(__file__).with_name("amendment2_access_intake.template.json")


def complete_intake():
    data = copy.deepcopy(load_intake(TEMPLATE))
    data.update(
        candidate_id="synthetic-controlled-candidate",
        review_date="2026-08-15",
        completed_by_role="data custodian",
        evidence_urls=["https://example.org/protocol"],
        notes="Metadata-only synthetic contract test.",
    )
    data["design"] = {
        "same_people_in_decline_and_recovery": "yes",
        "arm_labels": {"decline": "protocol decline", "recovery": "protocol recovery"},
        "observations_per_person": {"decline": 80, "recovery": 80},
        "time_unit": "prompt",
        "arm_boundary_source": "prospective protocol labels",
    }
    data["variables"] = {
        "observed_state": "yes",
        "agent_action_or_proxy": "yes",
        "external_forcing": "yes",
        "action_forcing_distinct": "yes",
        "bidirectional_forcing": "yes",
        "independent_non_self_report_endpoint": "yes",
    }
    data["access"] = {
        "route": "controlled_local_execution",
        "institutional_sponsor_required": "no",
        "ethics_approval_required": "no",
        "data_use_agreement_required": "yes",
        "institutional_route_status": "not_required",
        "local_offline_execution_possible": "yes",
        "contact_route": "official repository request form",
    }
    return data


class AccessIntakeValidationTests(unittest.TestCase):
    def test_blank_template_is_metadata_incomplete(self):
        report = evaluate_intake(load_intake(TEMPLATE))
        self.assertEqual(report["status"], "METADATA_INCOMPLETE")
        self.assertFalse(report["participant_data_access_authorized"])
        self.assertEqual(report["amendment2_verdict"], "NO AMENDMENT 2 VERDICT")

    def test_complete_metadata_only_intake_reaches_formal_review_only(self):
        report = evaluate_intake(complete_intake())
        self.assertEqual(report["status"], "ELIGIBLE_FOR_FORMAL_GOVERNANCE_REVIEW")
        self.assertEqual(report["d4_design_status"], "PASSES_METADATA_ONLY")
        self.assertEqual(report["amendment2_mapping_status"], "POTENTIALLY_MAPPABLE")
        self.assertFalse(report["participant_data_access_authorized"])

    def test_missing_same_person_arms_is_design_ineligible(self):
        data = complete_intake()
        data["design"]["same_people_in_decline_and_recovery"] = "no"
        report = evaluate_intake(data)
        self.assertEqual(report["status"], "DESIGN_INELIGIBLE")

    def test_fewer_than_50_observations_in_one_arm_is_design_ineligible(self):
        data = complete_intake()
        data["design"]["observations_per_person"]["recovery"] = 49
        report = evaluate_intake(data)
        self.assertEqual(report["d4_design_status"], "FAILED")

    def test_unconfirmed_institutional_route_requires_governance(self):
        data = complete_intake()
        data["access"]["institutional_sponsor_required"] = "yes"
        data["access"]["institutional_route_status"] = "not_confirmed"
        report = evaluate_intake(data)
        self.assertEqual(report["status"], "GOVERNANCE_REQUIRED")

    def test_impossible_local_execution_blocks_local_route(self):
        data = complete_intake()
        data["access"]["local_offline_execution_possible"] = "no"
        report = evaluate_intake(data)
        self.assertEqual(report["status"], "ACCESS_BLOCKED")

    def test_any_participant_data_transfer_triggers_safety_stop(self):
        data = complete_intake()
        data["safeguards"]["participant_level_data_transferred_to_vot_team"] = True
        report = evaluate_intake(data)
        self.assertEqual(report["status"], "SAFETY_STOP")
        self.assertFalse(report["participant_data_access_authorized"])


if __name__ == "__main__":
    unittest.main()
