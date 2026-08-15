import json
import tempfile
import unittest
from pathlib import Path

from simulations.reproduce_openesm_screen import ReproductionError, screen_metadata_files


class OpenESMScreenReproductionTests(unittest.TestCase):
    def test_screen_uses_declared_metadata_and_feature_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = root / "0001_metadata.json"
            second = root / "0002_metadata.json"
            first.write_text(
                json.dumps(
                    {
                        "dataset_id": "0001",
                        "topics": "affect",
                        "features": [{"coding": "baseline before therapy"}],
                    }
                ),
                encoding="utf-8",
            )
            second.write_text(
                json.dumps(
                    {
                        "dataset_id": "0002",
                        "additional_comments": "observational series",
                        "features": [],
                    }
                ),
                encoding="utf-8",
            )
            ids, shortlist = screen_metadata_files(
                [second, first], r"\b(therapy|baseline)\b"
            )
            self.assertEqual(ids, ["0001", "0002"])
            self.assertEqual(shortlist, ["0001"])

    def test_duplicate_dataset_ids_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = []
            for name in ("a_metadata.json", "b_metadata.json"):
                path = root / name
                path.write_text(
                    json.dumps({"dataset_id": "0001", "features": []}),
                    encoding="utf-8",
                )
                paths.append(path)
            with self.assertRaises(ReproductionError):
                screen_metadata_files(paths, r"therapy")


if __name__ == "__main__":
    unittest.main()
