from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import pandas as pd

from src.config import SETTINGS
from src.enrich import enrich_lead
from src.generate import generate_message
from src.sheets_logger import log_to_google_sheets


REQUIRED_COLUMNS = {
    "name",
    "company",
    "industry",
    "country",
    "company_size",
    "website",
    "contact_role",
}


def validate_input(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")


def process_leads(input_path: str) -> pd.DataFrame:
    df = pd.read_csv(input_path)
    validate_input(df)

    output_rows: list[dict] = []

    for row in df.to_dict(orient="records"):
        enriched = enrich_lead(
            industry=row["industry"],
            company_size=row["company_size"],
            role=row["contact_role"],
        )

        lead = {
            **row,
            "segment": enriched.segment,
            "pain_point": enriched.pain_point,
            "automation_angle": enriched.automation_angle,
            "priority_score": enriched.priority_score,
        }

        message = generate_message(lead)

        output_rows.append(
            {
                **lead,
                "email_subject": message["subject"],
                "email_body": message["body"],
                "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            }
        )

    return pd.DataFrame(output_rows)


def save_output(df: pd.DataFrame) -> Path:
    output_dir = Path(SETTINGS.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = f"enriched_outreach_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    output_path = output_dir / filename
    df.to_csv(output_path, index=False)
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI Revenue Agent: lead enrichment and outreach automation")
    parser.add_argument(
        "--input",
        default="data/leads_sample.csv",
        help="Path to input CSV file with leads",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result_df = process_leads(args.input)
    output_path = save_output(result_df)

    print(f"Saved CSV output to: {output_path}")

    if SETTINGS.google_sheets_enabled:
        log_to_google_sheets(result_df)
        print(
            "Logged results to Google Sheets: "
            f"{SETTINGS.google_sheets_spreadsheet} / {SETTINGS.google_sheets_worksheet}"
        )


if __name__ == "__main__":
    main()
