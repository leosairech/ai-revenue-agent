from __future__ import annotations

from pathlib import Path

import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

from src.config import SETTINGS

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def log_to_google_sheets(df: pd.DataFrame) -> None:
    creds_path = Path(SETTINGS.google_service_account_json)
    if not creds_path.exists():
        raise FileNotFoundError(
            f"Google service account file not found at: {creds_path}. "
            "Update GOOGLE_SERVICE_ACCOUNT_JSON in .env or disable Google Sheets logging."
        )

    credentials = Credentials.from_service_account_file(str(creds_path), scopes=SCOPES)
    client = gspread.authorize(credentials)

    try:
        spreadsheet = client.open(SETTINGS.google_sheets_spreadsheet)
    except gspread.SpreadsheetNotFound:
        spreadsheet = client.create(SETTINGS.google_sheets_spreadsheet)

    try:
        worksheet = spreadsheet.worksheet(SETTINGS.google_sheets_worksheet)
        worksheet.clear()
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=SETTINGS.google_sheets_worksheet, rows=100, cols=20)

    rows = [df.columns.tolist()] + df.fillna("").astype(str).values.tolist()
    worksheet.update(rows)
