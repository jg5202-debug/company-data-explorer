"""Small, reusable steps for cleaning and filtering company records."""

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
DEMO_PATH = ROOT / "demo_companies.json"
OUTPUT_PATH = ROOT / "outputs" / "filtered_companies.json"
REQUIRED_COLUMNS = {"name", "country_code", "region"}


def load_companies(path=None):
    """Read the fictional JSON demo or a user-provided CSV."""
    path = Path(path) if path is not None else DEMO_PATH
    if path.suffix.lower() == ".json":
        with path.open(encoding="utf-8") as file:
            df = pd.DataFrame(json.load(file))
    else:
        df = pd.read_csv(
            path,
            dtype={"name": "string", "country_code": "string", "region": "string"},
        )
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    return df


def clean_companies(df):
    """Remove missing, empty, and whitespace-only names; keep duplicates."""
    cleaned = df.dropna(subset=["name"]).copy()
    return cleaned[cleaned["name"].str.strip() != ""].copy()


def filter_companies(df):
    """Select US companies with an 'ad' prefix, ignoring letter case."""
    only_usa = df["country_code"] == "USA"
    starts_with_ad = df["name"].str.lower().str.startswith("ad", na=False)
    filtered = df[only_usa & starts_with_ad].copy()
    # name_length counts characters, including spaces and punctuation.
    filtered["name_length"] = filtered["name"].str.len()
    return filtered


def json_round_trip(df, path=OUTPUT_PATH):
    """Write row-oriented JSON and reload it, preserving empty-table columns."""
    records = json.loads(df.to_json(orient="records"))
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=2, allow_nan=False)
    with path.open(encoding="utf-8") as file:
        reloaded_records = json.load(file)
    reloaded = pd.DataFrame.from_records(reloaded_records, columns=df.columns)
    return records, reloaded


def new_york_companies(df):
    """Filter the reloaded data by region, not by city."""
    return df[df["region"] == "New York"].copy()

