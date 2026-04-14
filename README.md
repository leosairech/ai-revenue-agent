# AI Revenue Agent – Lead Enrichment & Outreach Automation

An applied AI project that simulates a real revenue operations workflow:

1. Reads leads from a CSV file
2. Enriches each lead with segment, pain point, automation angle, and priority score
3. Generates a personalized outbound email using an LLM or a local mock mode
4. Saves the output to CSV
5. Optionally logs the run to Google Sheets

---

## Tech stack

- Python
- Pandas
- OpenAI API (optional but recommended)
- Google Sheets via `gspread` and `google-auth` (optional)
- `.env` configuration with `python-dotenv`

---

## Project structure

```bash
ai_revenue_agent_repo/
├── data/
│   └── leads_sample.csv
├── output/
├── src/
│   ├── config.py
│   ├── enrich.py
│   ├── generate.py
│   ├── main.py
│   └── sheets_logger.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## How it works

### Input
The project expects a CSV with these columns:

- `name`
- `company`
- `industry`
- `country`
- `company_size`
- `website`
- `contact_role`

### Enrichment logic
Each lead is enriched with:

- `segment`
- `pain_point`
- `automation_angle`
- `priority_score`

### Message generation
The project supports two modes:

#### 1. Real mode
Uses the OpenAI API to generate a personalized outbound email.

#### 2. Demo mode
Uses a local deterministic template if you do not want to use the API yet.

---

## Setup

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd ai_revenue_agent_repo
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

#### Windows
```bash
.venv\Scripts\activate
```

#### macOS / Linux
```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create your `.env`

Copy `.env.example` to `.env` and edit it.

#### Demo mode
```env
USE_OPENAI=false
GOOGLE_SHEETS_ENABLED=false
```

#### Real mode
```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1-mini
USE_OPENAI=true
GOOGLE_SHEETS_ENABLED=false
```

---

## Run the project

Use the sample data:

```bash
python -m src.main
```

Or use your own CSV:

```bash
python -m src.main --input data/my_leads.csv
```

The project will generate a CSV file inside `output/`.

---

## Example output columns

- original lead fields
- `segment`
- `pain_point`
- `automation_angle`
- `priority_score`
- `email_subject`
- `email_body`
- `generated_at`

---

## Google Sheets logging (optional)

This project can also write the final output to Google Sheets.

### What you need

- A Google Cloud project
- Google Sheets API enabled
- Google Drive API enabled
- A service account JSON file
- The spreadsheet shared with the service account email

Service accounts are a standard way to authenticate server-to-server Google API access, and gspread supports using a service account for Sheets/Drive scopes. Also, a spreadsheet must be shared with that service account unless it is publicly accessible. citeturn260633search1turn260633search2turn260633search12

### Steps

1. Put the JSON credentials file in a local `credentials/` folder
2. Update `.env`:

```env
GOOGLE_SHEETS_ENABLED=true
GOOGLE_SHEETS_SPREADSHEET=AI Revenue Agent Logs
GOOGLE_SHEETS_WORKSHEET=run_logs
GOOGLE_SERVICE_ACCOUNT_JSON=credentials/google_service_account.json
```

3. Share the target spreadsheet with the service account email
4. Run the project normally

---
