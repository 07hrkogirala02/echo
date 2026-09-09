import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


def generate_gemini_explanation(investigation, hypothesis):
    """
    Generate a human-readable explanation of the investigation.

    Gemini explains the evidence produced by Echo's deterministic
    investigation engine. It does not independently calculate
    causal scores.
    """

    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION")

    if not project:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT is not configured.")

    if not location:
        location = "us-central1"

    client = genai.Client(
        vertexai=True,
        project=project,
        location=location,
    )

    deployment = investigation.get("deployment", {})

    system_impact = investigation.get("system_impact", [])
    product_impact = investigation.get("product_impact", [])
    business_impact = investigation.get("business_impact", [])

    evidence = hypothesis.get("evidence", {})
    hypotheses = hypothesis.get("hypotheses", [])
    competing_events = hypothesis.get("competing_events", [])

    prompt = f"""
You are Echo, a deployment investigation assistant.

Your job is to explain an investigation using ONLY the evidence
provided below.

IMPORTANT:
- Do not invent metrics.
- Do not invent events.
- Do not claim certainty when the evidence does not support it.
- Echo's deterministic investigation engine has already calculated
  the evidence score and hypothesis ranking.
- Your job is to explain the evidence clearly to a software engineer
  or product manager.
- Keep the explanation concise and actionable.

DEPLOYMENT

Deployment ID: {deployment.get("deployment_id")}
Service: {deployment.get("service")}
Version: {deployment.get("version")}
Feature: {deployment.get("feature")}
Environment: {deployment.get("environment")}
Deployment time: {deployment.get("deployment_time")}

EVIDENCE

Evidence score: {evidence.get("score")}
Evidence confidence: {evidence.get("confidence")}

Evidence components:
{evidence.get("components", {})}

SYSTEM IMPACT

{system_impact}

PRODUCT IMPACT

{product_impact}

BUSINESS IMPACT

{business_impact}

COMPETING EVENTS

{competing_events}

HYPOTHESES

{hypotheses}

Return the response using exactly these sections:

SUMMARY:
A 2-3 sentence explanation of what most likely happened.

WHY:
3-5 concise bullet points explaining the strongest evidence.

COMPETING_FACTORS:
Explain whether there are competing events and how they affect confidence.

RECOMMENDED_ACTION:
Give 1-3 practical next steps for the engineering team.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text