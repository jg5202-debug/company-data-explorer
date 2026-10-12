"""Focused tests using fictional data only."""

import json

import pandas as pd
import pytest

from app import create_app
from pipeline import (
    clean_companies,
    filter_companies,
    json_round_trip,
    load_companies,
    new_york_companies,
)


def test_demo_pipeline(tmp_path):
    raw = load_companies()
    cleaned = clean_companies(raw)
    filtered = filter_companies(cleaned)
    records, reloaded = json_round_trip(filtered, tmp_path / "companies.json")
    selected = new_york_companies(reloaded)
    assert (len(raw), len(cleaned), len(filtered), len(selected)) == (10, 7, 5, 4)
    assert isinstance(records, list)
    assert all(isinstance(record, dict) for record in records)
    assert len(filtered) == len(reloaded)
    assert list(filtered.columns) == list(reloaded.columns)
    assert reloaded["name"].tolist() == filtered["name"].tolist()
    assert "AdCafé Example" in reloaded["name"].tolist()
    assert all(filtered["name_length"] == filtered["name"].str.len())


def test_cleaning_keeps_duplicates_and_does_not_change_input():
    df = pd.DataFrame({"name": [None, "", "   ", "AdExample", "AdExample"]})
    original = df.copy(deep=True)
    cleaned = clean_companies(df)
    assert cleaned["name"].tolist() == ["AdExample", "AdExample"]
    pd.testing.assert_frame_equal(df, original)


def test_filter_is_case_insensitive_and_requires_usa():
    df = pd.DataFrame({
        "name": ["AdOne", "adTwo", "ADThree", "BadPrefix", "AdForeign", "AdMissing"],
        "country_code": ["USA", "USA", "USA", "USA", "CAN", None],
    })
    assert filter_companies(df)["name"].tolist() == ["AdOne", "adTwo", "ADThree"]


def test_empty_round_trip_preserves_columns(tmp_path):
    filtered = filter_companies(clean_companies(load_companies())).iloc[:0]
    records, reloaded = json_round_trip(filtered, tmp_path / "empty.json")
    assert records == []
    assert list(reloaded.columns) == list(filtered.columns)
    assert len(new_york_companies(reloaded)) == 0
    assert create_app(new_york_companies(reloaded)).test_client().get("/").status_code == 200


def test_region_not_city():
    df = pd.DataFrame({"region": ["New York", "California"], "city": ["Albany", "New York"]})
    assert new_york_companies(df)["city"].tolist() == ["Albany"]


def test_webpage_escapes_data():
    df = pd.DataFrame({"name": ['Ad<script>alert("demo")</script>']})
    response = create_app(df).test_client().get("/")
    html = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Row count: 1" in html
    assert "&lt;script&gt;" in html
    assert "<script>" not in html


def test_csv_input(tmp_path):
    path = tmp_path / "input.csv"
    pd.DataFrame({"name": ["AdExample"], "country_code": ["USA"], "region": ["New York"]}).to_csv(path, index=False)
    assert load_companies(path)["name"].tolist() == ["AdExample"]


def test_missing_columns_are_reported(tmp_path):
    path = tmp_path / "invalid.json"
    path.write_text(json.dumps([{"name": "Example"}]), encoding="utf-8")
    with pytest.raises(ValueError, match="Missing required columns"):
        load_companies(path)

