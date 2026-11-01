
import re
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from google import genai
from google.genai import types

from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load API configuration
Config.validate()
client = genai.Client(api_key=Config.GEMINI_API_KEY)

INDIA_TIMEZONE = ZoneInfo("Asia/Kolkata")


def get_india_datetime() -> datetime:
    """Get the actual current date and time in India."""
    return datetime.now(INDIA_TIMEZONE)


def is_datetime_question(prompt: str) -> bool:
    """Identify questions asking for today's date or current time."""
    text = prompt.lower()

    date_time_terms = [
        "today's date",
        "todays date",
        "current date",
        "today date",
        "current time",
        "time in india",
        "date and time",
        "what time is it",
        "what day is it",
    ]

    return any(term in text for term in date_time_terms)


def generate_chat_response(prompt: str) -> str:
    """Generate a response using Gemini and live Google Search grounding."""

    # Return date/time directly from Python to avoid AI date hallucinations.
    if is_datetime_question(prompt):
        now = get_india_datetime()

        return (
            f"Today's date is {now.strftime('%A, %B %d, %Y')}.\n\n"
            f"The current time in India is "
            f"{now.strftime('%I:%M:%S %p')} IST.\n\n"
            "Timezone: Indian Standard Time (IST), UTC+05:30."
        )

    # Calculate the date/time freshly for every other request.
    now = get_india_datetime()
    current_datetime = now.strftime(
        "%A, %d %B %Y, %I:%M:%S %p IST"
    )

    system_instruction = f"""
You are a helpful, accurate AI assistant.

CURRENT DATE AND TIME:
{current_datetime}

IMPORTANT RULES:
1. Treat the date and time above as the current date and time in India.
2. Never invent a different current date or time.
3. For current affairs, recent news, changing facts, and events,
   use Google Search grounding to find reliable, up-to-date sources.
4. Distinguish the date an event happened from the date an article
   was published.
5. Provide source names and source URLs when available.
6. Never invent headlines, events, statistics, quotations, or sources.
7. If you cannot verify a claim, clearly say so.
8. If the user asks about a past month or year, search for events
   from that specific period rather than treating them as future events.
9. Answer clearly and honestly. Do not claim to have searched the web
   if you have not obtained search-grounded information.
"""

    try:
        response = client.models.generate_content(
            model=Config.MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=[
                    types.Tool(
                        google_search=types.GoogleSearch()
                    )
                ],
            ),
        )

        if response.text:
            return response.text

        logger.warning("Gemini returned an empty response.")
        return "I couldn't generate a response. Please try again."

    except Exception:
        logger.exception("Gemini response generation failed")
        return (
            "Sorry, I couldn't process your request right now. "
            "Please try again or check the backend terminal logs."
        )
