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


if __name__ == "__main__":
    unittest.main()
