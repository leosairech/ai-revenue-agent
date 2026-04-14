from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EnrichedLead:
    segment: str
    pain_point: str
    automation_angle: str
    priority_score: int


def infer_segment(industry: str, company_size: str) -> str:
    industry_key = industry.strip().lower()
    size_key = company_size.strip().lower()

    if "security" in industry_key:
        return "Physical Security / Surveillance"
    if "retail" in industry_key:
        return "Retail Operations"
    if "logistics" in industry_key:
        return "Supply Chain / Logistics"
    if "fintech" in industry_key:
        return "Financial Services"
    if "saas" in industry_key:
        return "B2B SaaS"

    if "enterprise" in size_key:
        return "Large Enterprise"
    if "startup" in size_key:
        return "Startup / Early Growth"
    return "General B2B"


def infer_pain_point(industry: str, role: str) -> str:
    industry_key = industry.strip().lower()
    role_key = role.strip().lower()

    if "security" in industry_key:
        return "slow lead qualification and fragmented follow-up across distributors"
    if "retail" in industry_key:
        return "manual campaign execution and poor visibility into conversion bottlenecks"
    if "logistics" in industry_key:
        return "disconnected customer data and inefficient outbound coordination"
    if "fintech" in industry_key:
        return "high volume of inbound interest with limited personalization at scale"
    if "saas" in industry_key:
        return "inconsistent prospecting workflows and weak lead enrichment"

    if "ceo" in role_key:
        return "too much founder time spent on repetitive outreach"
    if "operations" in role_key:
        return "manual handoffs between commercial and operational teams"
    return "manual sales operations and limited workflow automation"


def infer_automation_angle(industry: str) -> str:
    industry_key = industry.strip().lower()

    if "security" in industry_key:
        return "AI agent for distributor lead qualification, routing, and personalized outreach"
    if "retail" in industry_key:
        return "AI workflows for campaign personalization and follow-up automation"
    if "logistics" in industry_key:
        return "AI-assisted revenue ops automation across prospecting and follow-up"
    if "fintech" in industry_key:
        return "AI-driven lead triage and tailored first-touch messaging"
    if "saas" in industry_key:
        return "automated lead enrichment and outbound personalization"
    return "revenue workflow automation using AI agents and integrated business tools"


def infer_priority_score(company_size: str, role: str) -> int:
    size_key = company_size.strip().lower()
    role_key = role.strip().lower()

    score = 50
    if "enterprise" in size_key:
        score += 25
    elif "mid" in size_key:
        score += 15
    elif "startup" in size_key:
        score += 10

    if any(keyword in role_key for keyword in ["director", "head", "ceo", "owner"]):
        score += 20
    elif "manager" in role_key:
        score += 10

    return min(score, 100)


def enrich_lead(industry: str, company_size: str, role: str) -> EnrichedLead:
    return EnrichedLead(
        segment=infer_segment(industry, company_size),
        pain_point=infer_pain_point(industry, role),
        automation_angle=infer_automation_angle(industry),
        priority_score=infer_priority_score(company_size, role),
    )
