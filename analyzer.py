import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_sentiment(text: str, model: str = "gpt-4.1-mini"):
    """
    Runs a sentiment analysis.
    Returns a dict with {label, explanation, raw_response}.
    """

    prompt = f"""
Analyze the sentiment of the following text and respond ONLY with valid JSON using this structure:

{{
  "label": "positive|negative|neutral",
  "explanation": "short explanation of why"
}}

Text: {text}
"""

    try:
        response = client.responses.create(
            model=model,
            input=prompt,
        )

        # Correct way: ensures consistent extraction
        raw = response.output_text

        # Clean raw text (remove backticks, whitespace)
        raw_clean = raw.strip().replace("```json", "").replace("```", "").strip()

        # Try JSON parse
        try:
            data = json.loads(raw_clean)
            label = data.get("label", "neutral").lower()

        except Exception:
            raw_lower = raw.lower()
            if "positive" in raw_lower:
                label = "positive"
            elif "negative" in raw_lower:
                label = "negative"
            else:
                label = "neutral"

            data = {
                "label": label,
                "explanation": raw_clean
            }

        return {
            "label": label,
            "explanation": data.get("explanation", ""),
            "raw_response": raw_clean,
        }

    except Exception as e:
        return {
            "label": "error",
            "explanation": "",
            "raw_response": f"Error while calling model: {str(e)}"
        }
