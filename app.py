"""Run a local Flask webpage using the same pipeline as the notebook."""

import argparse

from flask import Flask

from pipeline import (
    clean_companies,
    filter_companies,
    json_round_trip,
    load_companies,
    new_york_companies,
)


def create_app(companies):
    app = Flask(__name__)

    @app.route("/")
    def show_companies():
        # An HTML table makes the selected company details easy to compare.
        return (
            "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            "<title>Company Data Explorer</title></head><body>"
            "<h1>Company Data Explorer</h1>"
            "<p>US companies starting with ad in the New York region.</p>"
            f"<p>Row count: {len(companies)}</p>"
            + companies.to_html(index=False, escape=True)
            + "</body></html>"
        )

    return app


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", help="Optional local CSV; otherwise use fictional demo data.")
    parser.add_argument("--port", type=int, default=5002)
    args = parser.parse_args()

    raw = load_companies(args.csv)
    cleaned = clean_companies(raw)
    filtered = filter_companies(cleaned)
    records, reloaded = json_round_trip(filtered)
    selected = new_york_companies(reloaded)
    print(f"Input rows: {len(raw)}")
    print(f"Cleaned rows: {len(cleaned)}")
    print(f"Filtered rows / JSON objects: {len(records)}")
    print(f"Row counts match: {len(filtered) == len(reloaded)}")
    print(f"New York region rows: {len(selected)}")
    create_app(selected).run(host="127.0.0.1", port=args.port, debug=False)


if __name__ == "__main__":
    main()

