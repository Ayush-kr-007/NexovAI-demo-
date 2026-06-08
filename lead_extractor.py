import json
import os
import re
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_lead(conversation):
    if not conversation.strip():
        return {
            "call_handling": "", "daily_calls": "", "industry": "",
            "interest": "", "budget": "", "timeline": ""
        }

    prompt = f"""
Extract lead information from this sales conversation.
Return ONLY a raw JSON object. No markdown, no code blocks, no explanation.

Schema:
{{
    "call_handling": "",
    "daily_calls": "",
    "industry": "",
    "interest": "",
    "budget": "",
    "timeline": ""
}}

Conversation:
{conversation}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    raw = response.choices[0].message.content.strip()

    # Strip markdown code fences if present
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    raw = raw.strip()

    return json.loads(raw)