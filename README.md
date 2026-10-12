# Company Data Explorer

A small Python learning project by **Junyu Gai**. It reads company records, cleans company names, applies a case-insensitive filter, writes and reloads JSON, and displays selected records in a local Flask webpage.

The public version uses **fictional demo companies**, not real Crunchbase records. It adapts a personal coursework exercise for a standalone demonstration; course handouts, assignment instructions, recordings, and original data are not included.

## What it does

1. Load data and remove missing, empty, or whitespace-only company names.
2. Keep US companies whose names start with `ad`, ignoring letter case; add `name_length`.
3. Save a list of row objects as JSON and reload it into a new DataFrame.
4. Filter by the **New York region** and serve an HTML table with Flask.

Duplicates are deliberately retained. Removing blank names does not trim valid names. `name_length` counts characters, including spaces and punctuation. The notebook's row-count check confirms record-count preservation, not full value or dtype equality.

## Quick start

Requires Python 3.10 or newer. Run commands from the project directory.

```bash
git clone https://github.com/jg5202-debug/company-data-explorer.git
cd company-data-explorer
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5002/** in your browser. Stop the server with `Ctrl+C`.

Expected results for the bundled fictional dataset: **10 input rows, 7 cleaned rows, 5 filtered rows/JSON objects, and 4 New York-region rows**. Generated JSON is saved under `outputs/`, which is ignored by Git.

If the port is occupied, use `python app.py --port 5003` and visit the matching port. This is a local development demo, not a deployed or production-ready service. Uploading source code to GitHub does not automatically host the Flask app.

## Explore the notebook

```bash
python -m pip install -r requirements-dev.txt
jupyter notebook company_explorer.ipynb
```

Select the Python environment containing the dependencies, then run the cells in order. The notebook shows each data-processing step and checks the Flask response without starting a blocking server cell. Use `python app.py` in a separate terminal to visit the live webpage.

## Use your own CSV

```bash
python app.py --csv data/companies.csv
```

Required columns: `name`, `country_code`, and `region`. Other columns are preserved. US records must use the country code `USA`; the region filter matches `New York` exactly. Only use data you are authorized to access and process.

Local CSV files and the `data/` directory are ignored by Git. The repository does not redistribute or grant rights to any third-party dataset. In the notebook, set `INPUT_PATH` to your own CSV path instead of `None`.

## Files

- `company_explorer.ipynb`: step-by-step walkthrough with fictional sample outputs.
- `pipeline.py`: reusable load, clean, filter, and JSON round-trip functions.
- `app.py`: local Flask webpage and command-line entry point.
- `demo_companies.json`: 10 fictional records, including deliberate missing and blank names.
- `test_project.py`: tests for filtering, JSON, empty results, and escaped HTML.

## Tests

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

The tests use fictional records only. They check representative values and column preservation as well as row counts; they do not claim that JSON preserves every possible Pandas dtype.

## Learning focus

Pandas boolean indexing, string operations, missing-value handling, JSON `records` orientation, and Flask routes. This project demonstrates a small end-to-end data workflow rather than a business analysis or production data platform.

