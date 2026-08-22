import copy
import csv
import json
import tempfile
import unittest
from pathlib import Path

from simulations.amendment2_reference_harness import (
    HARNESS_STATUS,
    MODEL_IDS,
    build_audit,
    generate_scenario,
    run_replicate,
    run_registry,
    split_transitions,
    write_results,
)
from simulations.validate_scenario_registry import load_registry


REGISTRY = Path(__file__).with_name("amendment2_scenarios.v0.json")


def compact_scenario(scenario_id):
    registry = load_registry(REGISTRY)
    scenario = copy.deepcopy(next(item for item in registry["calibration_scenarios"] if item["id"] == scenario_id))
    scenario["cases"] = 4
    scenario["observations_per_arm"] = 50
    return scenario


class ReferenceHarnessTests(unittest.TestCase):
    def test_generation_is_deterministic_and_keeps_action_forcing_separate(self):
        scenario = compact_scenario("r1_smooth_moderate_noise")
        first = generate_scenario(scenario, 99)
        second = generate_scenario(scenario, 99)
        self.assertEqual(first, second)
        self.assertTrue(first)
        self.assertTrue(all(row.action in {-1, 1} for row in first))
        self.assertTrue(any(abs(row.forcing) not in {0.0, 1.0} for row in first))

    def test_chronological_split_is_disjoint_inside_each_unit(self):
        scenario = compact_scenario("r1_smooth_moderate_noise")
        train, validation, test = split_transitions(generate_scenario(scenario, 101))
        self.assertTrue(train and validation and test)
        for unit in {row.unit_key for row in train + validation + test}:
            train_times = [row.t for row in train if row.unit_key == unit]
            validation_times = [row.t for row in validation if row.unit_key == unit]
            test_times = [row.t for row in test if row.unit_key == unit]
            self.assertLess(max(train_times), min(validation_times))
            self.assertLess(max(validation_times), min(test_times))

    def test_reference_harness_separates_strong_fold_and_smooth_nonfold(self):
        smooth = run_replicate(compact_scenario("r1_smooth_moderate_noise"), replicate=1)
        fold = run_replicate(compact_scenario("vot_shared_fold_strong"), replicate=1)
        self.assertEqual(smooth["disposition"], "NO_FOLD")
        self.assertEqual(fold["disposition"], "FOLD")
        self.assertEqual(fold["best_fold_model"], "VOT")
        self.assertEqual(fold["d5_reference_disposition"], "VOT_PREFERRED_REFERENCE")
        self.assertFalse(smooth["verdict_authorized"])
        self.assertFalse(fold["verdict_authorized"])
        self.assertEqual({item["model_id"] for item in fold["models"]}, set(MODEL_IDS))
        self.assertTrue(all(item["test_occasions"] == fold["test_rows"] for item in fold["models"]))

    def test_vot_is_global_while_r6_uses_case_level_partial_pooling(self):
        result = run_replicate(compact_scenario("vot_shared_fold_strong"), replicate=1)
        models = {item["model_id"]: item for item in result["models"]}
        self.assertEqual(models["VOT"]["parameter_count"], 5)
        self.assertGreater(models["R6"]["parameter_count"], models["VOT"]["parameter_count"])
        self.assertTrue(models["VOT"]["fold_admissible"])

    def test_heterogeneous_r6_can_absorb_the_shared_vot_candidate(self):
        result = run_replicate(compact_scenario("r6_fold_strong"), replicate=1)
        self.assertEqual(result["disposition"], "FOLD")
        self.assertEqual(result["best_rival_model"], "R6")
        self.assertLess(result["vot_vs_best_rival_gap"], 0.0)
        self.assertEqual(result["d5_reference_disposition"], "ABSORBED_BY_RIVAL")

    def test_registry_runner_and_outputs_preserve_method_only_boundary(self):
        registry = load_registry(REGISTRY)
        results = run_registry(
            registry,
            replicates=1,
            scenario_ids={"r1_smooth_moderate_noise", "vot_shared_fold_strong"},
            cases_cap=4,
            observations_cap=50,
        )
        self.assertEqual(len(results), 2)
        audit = build_audit(results, margin=0.0)
        self.assertEqual(audit["status"], HARNESS_STATUS)
        self.assertFalse(audit["amendment2_verdict_authorized"])
        self.assertIn("selected VOT reference estimator", " ".join(audit["limitations"]))
        json.dumps(audit, allow_nan=False)

        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "results.csv"
            write_results(output, results)
            with output.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual({row["truth"] for row in rows}, {"FOLD", "NON_FOLD"})
            self.assertTrue(all(row["harness_status"] == HARNESS_STATUS for row in rows))
            self.assertTrue(all(row["verdict_authorized"] == "False" for row in rows))
            self.assertTrue(all(row["d5_reference_disposition"] for row in rows))

    def test_too_short_scenario_is_underpowered_not_a_model_win(self):
        scenario = compact_scenario("r6_fold_strong")
        scenario["observations_per_arm"] = 6
        result = run_replicate(scenario, replicate=1)
        self.assertEqual(result["disposition"], "UNDERPOWERED")
        self.assertEqual(result["winning_model"], "")


if __name__ == "__main__":
    unittest.main()
