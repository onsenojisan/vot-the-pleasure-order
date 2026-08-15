import copy
import unittest
from pathlib import Path

from simulations.reproduce_zenodo_screen import ReproductionError, reproduce_zenodo_search
from simulations.validate_dataset_screening import load_screening


REGISTRY = Path(__file__).with_name("amendment2_dataset_screening.v0.json")


class ZenodoScreenReproductionTests(unittest.TestCase):
    def setUp(self):
        data = load_screening(REGISTRY)
        self.search = data["additional_catalogue_searches"][0]

    def _frozen_fetcher(self, _api_url, query_text, _size, _sort):
        query = next(item for item in self.search["queries"] if item["q"] == query_text)
        return {
            "hits": {
                "total": query["declared_total"],
                "hits": [{"id": int(record_id)} for record_id in query["record_ids"]],
            }
        }

    def test_frozen_query_results_match(self):
        report = reproduce_zenodo_search(self.search, self._frozen_fetcher)
        self.assertEqual(report["status"], "MATCHES_FROZEN_SEARCH")
        self.assertEqual(report["union_record_count"], 5)

    def test_changed_record_set_is_reported_as_drift(self):
        def changed_fetcher(api_url, query_text, size, sort):
            payload = self._frozen_fetcher(api_url, query_text, size, sort)
            if query_text == self.search["queries"][0]["q"]:
                payload = copy.deepcopy(payload)
                payload["hits"]["hits"] = [{"id": 999}]
            return payload

        with self.assertRaises(ReproductionError):
            reproduce_zenodo_search(self.search, changed_fetcher)

    def test_total_beyond_page_size_requires_pagination(self):
        search = copy.deepcopy(self.search)
        search["request_parameters"]["size"] = 1
        search["queries"][2]["declared_total"] = 4
        with self.assertRaises(ReproductionError):
            reproduce_zenodo_search(search, self._frozen_fetcher)


if __name__ == "__main__":
    unittest.main()
