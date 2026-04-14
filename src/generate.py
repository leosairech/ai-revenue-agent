from __future__ import annotations

import textwrap
from openai import OpenAI

from src.config import SETTINGS


def build_prompt(lead: dict) -> str:
    return textwrap.dedent(
        f"""
        You are a senior revenue operations strategist specializing in AI-driven automation.

        Your task is to generate a highly personalized outbound message for a business lead.

        Prospect details:
        - Name: {lead['name']}
        - Company: {lead['company']}
        - Industry: {lead['industry']}
        - Contact role: {lead['contact_role']}
        - Segment: {lead['segment']}
        - Priority score: {lead['priority_score']}
        - Main pain point: {lead['pain_point']}
        - Automation angle: {lead['automation_angle']}

        Instructions:

1. Write a concise, high-quality outbound email (max 120-150 words).
2. Avoid generic phrases like "reduce manual work" or "improve efficiency".
3. Include ONE concrete operational insight relevant to the industry or role.
   - Example: delays in lead qualification, fragmented distributor pipelines, lack of visibility, etc.
4. Make the message feel like it was written by a revenue operator, not an AI assistant.
5. Tailor tone based on role:
   - CEO → strategic and growth-focused
   - Operations → efficiency and execution
   - Growth/Marketing → conversion and scaling
6. Mention the company name naturally.
7. Frame the automation_angle as a practical, realistic opportunity (not hype).
8. Use a soft, consultative CTA (not pushy).
9. Do NOT use buzzwords or exaggerated claims.
10. Keep it natural, professional, and specific.

Output format:

Subject: <short, relevant subject line>

Email:
<email body>
        """
    ).strip()


def mock_generate_message(lead: dict) -> dict[str, str]:
    subject = f"Idea to automate {lead['company']}'s lead follow-up"
    body = (
        f"Hi {lead['name']},\n\n"
        f"I noticed that teams in {lead['industry']} often struggle with {lead['pain_point']}. "
        f"A practical opportunity for {lead['company']} could be {lead['automation_angle'].lower()}, "
        f"helping your team reduce manual work and improve response speed. "
        f"Given your role as {lead['contact_role']}, this could be especially useful if you're looking to scale outreach "
        f"without adding more operational overhead.\n\n"
        f"Would you be open to a 15-minute call next week to explore whether this could fit your workflow?\n\n"
        "Best,\nLeonel"
    )
    return {"subject": subject, "body": body}


def openai_generate_message(lead: dict) -> dict[str, str]:
    if not SETTINGS.openai_api_key:
        raise ValueError("OPENAI_API_KEY is missing. Set it in your .env file.")

    client = OpenAI(api_key=SETTINGS.openai_api_key)
    response = client.responses.create(
        model=SETTINGS.openai_model,
        input=build_prompt(lead),
        text={"format": {"type": "json_schema", "name": "email_output", "schema": {
            "type": "object",
            "properties": {
                "subject": {"type": "string"},
                "body": {"type": "string"}
            },
            "required": ["subject", "body"],
            "additionalProperties": False
        }}},
    )

    json_text = response.output_text
    import json

    parsed = json.loads(json_text)
    return {"subject": parsed["subject"], "body": parsed["body"]}


def generate_message(lead: dict) -> dict[str, str]:
    if SETTINGS.use_openai:
        return openai_generate_message(lead)
    return mock_generate_message(lead)
