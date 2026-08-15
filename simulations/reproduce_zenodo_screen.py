#!/usr/bin/env python3
"""Re-run the frozen Zenodo queries and report any search-index drift."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlencode
from urllib.request import Request, urlopen

try:
    from simulations.validate_dataset_screening import load_screening, validate_screening
except ModuleNotFoundError:
    from validate_dataset_screening import load_screening, validate_screening


class ReproductionError(ValueError):
    pass


Fetcher = Callable[[str, str, int, str], dict[str, Any]]


def fetch_zenodo(api_url: str, query: str, size: int, sort: str) -> dict[str, Any]:
    url = f"{api_url}?{urlencode({'q': query, 'size': size, 'sort': sort})}"
    request = Request(url, headers={"User-Agent": "vot-amendment2-screen/0.1"})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def _total_value(raw_total: Any) -> int:
    if isinstance(raw_total, int):
        return raw_total
    if isinstance(raw_total, dict) and isinstance(raw_total.get("value"), int):
        return raw_total["value"]
    raise ReproductionError(f"unexpected Zenodo hits.total value: {raw_total!r}")


def reproduce_zenodo_search(
    search: dict[str, Any], fetcher: Fetcher = fetch_zenodo
) -> dict[str, Any]:
    parameters = search["request_parameters"]
    api_url = search["api_url"]
    size = parameters["size"]
    sort = parameters["sort"]
    observed_union: set[str] = set()
    query_reports: list[dict[str, Any]] = []

    for query in search["queries"]:
        payload = fetcher(api_url, query["q"], size, sort)
        hits_container = payload.get("hits")
        if not isinstance(hits_container, dict):
            raise ReproductionError(f"{query['query_id']}: response has no hits object")
        total = _total_value(hits_container.get("total"))
        hits = hits_container.get("hits")
        if not isinstance(hits, list):
            raise ReproductionError(f"{query['query_id']}: response hits must be an array")
        record_ids = {
            str(hit.get("id"))
            for hit in hits
            if isinstance(hit, dict) and hit.get("id") is not None
        }
        expected_ids = set(query["record_ids"])
        if total > size:
            raise ReproductionError(
                f"{query['query_id']}: total {total} exceeds frozen page size {size}; "
                "pagination is required before the result can be compared"
            )
        if total != query["declared_total"] or record_ids != expected_ids:
            raise ReproductionError(
                f"{query['query_id']}: search drift "
                f"(expected total={query['declared_total']}, ids={sorted(expected_ids)}; "
                f"observed total={total}, ids={sorted(record_ids)})"
            )
        observed_union.update(record_ids)
        query_reports.append(
            {"query_id": query["query_id"], "total": total, "record_ids": sorted(record_ids)}
        )

    expected_union = set(search["union_record_ids"])
    if observed_union != expected_union:
        raise ReproductionError(
            f"union drift (expected={sorted(expected_union)}, observed={sorted(observed_union)})"
        )
    return {
        "source_id": search["source_id"],
        "search_date": search["search_date"],
        "queries": query_reports,
        "union_record_count": len(observed_union),
        "union_record_ids": sorted(observed_union),
        "status": "MATCHES_FROZEN_SEARCH",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("registry", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    data = load_screening(args.registry)
    validate_screening(data)
    searches = [
        search
        for search in data["additional_catalogue_searches"]
        if search.get("source_id") == "zenodo"
    ]
    if len(searches) != 1:
        raise SystemExit("screening error: registry must contain exactly one Zenodo search")
    try:
        report = reproduce_zenodo_search(searches[0])
    except (OSError, ReproductionError) as exc:
        raise SystemExit(f"Zenodo reproduction error: {exc}") from exc
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
