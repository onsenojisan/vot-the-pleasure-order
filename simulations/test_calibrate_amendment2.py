import unittest

from simulations.calibrate_amendment2 import summarize, wilson_interval


def rows_for(scenario, truth, dispositions):
    return [
        {
            "scenario_id": scenario,
            "truth": truth,
            "replicate": str(index),
            "disposition": disposition,
        }
        for index, disposition in enumerate(dispositions, start=1)
    ]


class CalibrationTests(unittest.TestCase):
    def test_wilson_interval_contains_observed_rate(self):
        lower, upper = wilson_interval(80, 100)
        self.assertLess(lower, 0.80)
        self.assertGreater(upper, 0.80)

    def test_two_sided_report_passes_loose_test_targets(self):
        rows = []
        rows.extend(rows_for("fold", "FOLD", ["FOLD"] * 96 + ["NO_FOLD"] * 2 + ["TIE"] * 2))
        rows.extend(
            rows_for("smooth", "NON_FOLD", ["NO_FOLD"] * 96 + ["FOLD"] * 2 + ["UNDERPOWERED"] * 2)
        )
        report = summarize(rows, power_floor=0.85, false_error_ceiling=0.08, mcse_ceiling=0.05)
        self.assertTrue(report["both_truth_families_present"])
        self.assertTrue(report["overall_pass"])

    def test_missing_truth_family_blocks_overall_pass(self):
        rows = rows_for("fold", "FOLD", ["FOLD"] * 100)
        report = summarize(rows, power_floor=0.85, false_error_ceiling=0.08, mcse_ceiling=0.05)
        self.assertFalse(report["both_truth_families_present"])
        self.assertFalse(report["overall_pass"])


if __name__ == "__main__":
    unittest.main()
