import copy
import unittest
from pathlib import Path

from simulations.validate_scenario_registry import RegistryError, load_registry, validate_registry


REGISTRY = Path(__file__).with_name("amendment2_scenarios.v0.json")


class RegistryValidationTests(unittest.TestCase):
    def test_current_registry_is_valid_but_not_locked(self):
        report = validate_registry(load_registry(REGISTRY))
        self.assertEqual(report["status"], "VALID_DRAFT")
        self.assertFalse(report["locked_validation_ready"])
        self.assertEqual(set(report["truths_present"]), {"FOLD", "NON_FOLD"})

    def test_missing_active_inference_action_stream_fails(self):
        data = load_registry(REGISTRY)
        broken = copy.deepcopy(data)
        scenario = next(item for item in broken["calibration_scenarios"] if item["generator"] == "R4")
        scenario["action_stream"] = "absent"
        with self.assertRaises(RegistryError):
            validate_registry(broken)

    def test_missing_required_generator_fails(self):
        data = load_registry(REGISTRY)
        broken = copy.deepcopy(data)
        broken["calibration_scenarios"] = [
            item for item in broken["calibration_scenarios"] if item["generator"] != "R2"
        ]
        with self.assertRaises(RegistryError):
            validate_registry(broken)

    def test_r0_is_required_as_a_fitted_baseline_but_not_a_generator(self):
        data = load_registry(REGISTRY)
        self.assertNotIn("R0", {item["generator"] for item in data["calibration_scenarios"]})
        broken = copy.deepcopy(data)
        del broken["models"]["R0"]
        with self.assertRaises(RegistryError):
            validate_registry(broken)

    def test_vot_model_and_generator_are_required_for_p0_development(self):
        data = load_registry(REGISTRY)
        self.assertIn("VOT", data["models"])
        self.assertIn("VOT", {item["generator"] for item in data["calibration_scenarios"]})

        missing_model = copy.deepcopy(data)
        del missing_model["models"]["VOT"]
        with self.assertRaises(RegistryError):
            validate_registry(missing_model)

        missing_generator = copy.deepcopy(data)
        missing_generator["calibration_scenarios"] = [
            item for item in missing_generator["calibration_scenarios"] if item["generator"] != "VOT"
        ]
        with self.assertRaises(RegistryError):
            validate_registry(missing_generator)

    def test_fold_parameters_and_r6_heterogeneity_are_validated(self):
        data = load_registry(REGISTRY)

        invalid_vot = copy.deepcopy(data)
        vot = next(item for item in invalid_vot["calibration_scenarios"] if item["generator"] == "VOT")
        vot["parameters"]["delta"] = 0
        with self.assertRaises(RegistryError):
            validate_registry(invalid_vot)

        invalid_r6 = copy.deepcopy(data)
        r6 = next(item for item in invalid_r6["calibration_scenarios"] if item["generator"] == "R6")
        del r6["parameters"]["hierogeneity_sd"]
        with self.assertRaises(RegistryError):
            validate_registry(invalid_r6)


if __name__ == "__main__":
    unittest.main()
