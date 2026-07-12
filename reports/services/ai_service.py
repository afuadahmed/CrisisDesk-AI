import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field


load_dotenv()


class TriageResult(BaseModel):
    category: str
    urgency: str
    summary: str
    suggestedAction: str
    confidence: float = Field(ge=0, le=1)


def classify_report(description, location, language):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an emergency and public-service report triage system.

Analyze the citizen report below.

Description: {description}
Location: {location}
Language: {language}

The category must be exactly one of:
medical, fire, accident, crime, flood, utility,
public_service, infrastructure, other.

The urgency must be exactly one of:
low, medium, high, critical.

Assess urgency based on immediate danger to life, people trapped,
active violence, major hazards, and severity.

Write a short factual summary.
Recommend a concise action for responders.
Return a confidence score between 0 and 1.
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=TriageResult,
            temperature=0.1,
        ),
    )

    result = TriageResult.model_validate_json(response.text)

    return result.model_dump()