import copy
import unittest
from pathlib import Path

from simulations.preflight_amendment2 import evaluate_manifest, load_manifest


TEMPLATE = Path(__file__).with_name("amendment2_data_manifest.template.json")


def complete_manifest():
    data = copy.deepcopy(load_manifest(TEMPLATE))
    data["dataset_id"] = "synthetic-contract-test"
    data["prospective_status"]["variable_mapping_frozen"] = True
    data["design"].update(
        cases=32,
        time_unit="decision occasion",
        missing_data_rule="missing at random sensitivity plus declared informative-dropout scenario",
        irregular_timing_rule="elapsed time enters transition model",
    )
    data["design"]["observations_per_arm"] = {"decline": 100, "recovery": 100}
    data["variables"]["observed_state"] = {"names": ["y"], "mapping": "z-scored frozen channel"}
    data["variables"]["agent_action"] = {
        "status": "observed",
        "name": "a",
        "prospectively_justified": True,
        "proxy_justification": "not a proxy",
    }
    data["variables"]["external_forcing"] = {
        "status": "observed",
        "name": "u",
        "exogenous": True,
        "bidirectional": True,
        "coverage": "crosses declared structural domain in both directions",
    }
    data["variables"]["endpoint"] = {"status": "observed", "name": "endpoint"}
    data["separation"]["action_distinct_from_external_forcing"] = True
    data["parameterization"] = {
        "latent_state_dimension_grid": [1, 2],
        "action_set": [-1, 0, 1],
        "policy_horizon_grid": [1, 3],
        "prior_sensitivity_grid": ["weak", "regularizing"],
    }
    return data


class Amendment2PreflightTests(unittest.TestCase):
    def test_template_is_incomplete_and_never_claims_runnable(self):
        report = evaluate_manifest(load_manifest(TEMPLATE))
        self.assertEqual(report["status"], "INCOMPLETE")
        self.assertFalse(report["necessary_conditions_met"])
        self.assertFalse(report["runnable_claimed"])

    def test_complete_manifest_only_clears_necessary_conditions(self):
        report = evaluate_manifest(complete_manifest())
        self.assertEqual(report["status"], "NECESSARY_CONDITIONS_MET_NOT_SUFFICIENT")
        self.assertTrue(report["necessary_conditions_met"])
        self.assertFalse(report["runnable_claimed"])

    def test_absent_action_blocks_d5(self):
        data = complete_manifest()
        data["variables"]["agent_action"]["status"] = "absent"
        report = evaluate_manifest(data)
        self.assertEqual(report["status"], "HARD_BLOCKED")
        self.assertIn("ACTION_STREAM_ABSENT", {item["code"] for item in report["blockers"]})

    def test_same_variable_cannot_be_action_and_forcing(self):
        data = complete_manifest()
        data["variables"]["external_forcing"]["name"] = "a"
        report = evaluate_manifest(data)
        self.assertIn("ACTION_FORCING_CONFLATED", {item["code"] for item in report["blockers"]})

    def test_unidirectional_forcing_blocks_structure(self):
        data = complete_manifest()
        data["variables"]["external_forcing"]["bidirectional"] = False
        report = evaluate_manifest(data)
        blocker = next(item for item in report["blockers"] if item["code"] == "FORCING_NOT_BIDIRECTIONAL")
        self.assertEqual(blocker["scope"], "STRUCTURE")

    def test_prior_outcome_inspection_blocks_ratification(self):
        data = complete_manifest()
        data["prospective_status"]["target_outcomes_inspected_before_freeze"] = True
        report = evaluate_manifest(data)
        self.assertIn("TARGET_OUTCOME_ALREADY_INSPECTED", {item["code"] for item in report["blockers"]})

    def test_absent_endpoint_blocks_p3_only(self):
        data = complete_manifest()
        data["variables"]["endpoint"]["status"] = "absent"
        report = evaluate_manifest(data)
        blocker = next(item for item in report["blockers"] if item["code"] == "ENDPOINT_ABSENT")
        self.assertEqual(blocker["scope"], "P3")


if __name__ == "__main__":
    unittest.main()
