from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    use_openai: bool = os.getenv("USE_OPENAI", "true").lower() == "true"
    output_dir: str = os.getenv("OUTPUT_DIR", "output")
    google_sheets_enabled: bool = os.getenv("GOOGLE_SHEETS_ENABLED", "false").lower() == "true"
    google_sheets_spreadsheet: str = os.getenv("GOOGLE_SHEETS_SPREADSHEET", "AI Revenue Agent Logs")
    google_sheets_worksheet: str = os.getenv("GOOGLE_SHEETS_WORKSHEET", "run_logs")
    google_service_account_json: str = os.getenv(
        "GOOGLE_SERVICE_ACCOUNT_JSON", "credentials/google_service_account.json"
    )


SETTINGS = Settings()
