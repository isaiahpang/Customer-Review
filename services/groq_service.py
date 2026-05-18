from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME

# Initialize the Groq client using the key from config
client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = (
    "You are a database-integrated text processing utility. Analyze the user text data. "
    "You MUST output your response in a strict formatted style containing two sections:\n"
    "1. A bulleted summary synthesized from the reviews.\n"
    "2. A standalone single line stating exactly: 'FINAL_RATING: X' (where X is an integer score from 0 to 10).\n\n"
    "Keep your response analytical and professional."
)


def analyze_review_sentiment(review_content: str) -> dict:
    """
    Sends review text to Groq, extracts the rating, determines the category,
    and returns a dict with keys: summary, rating, category.
    """
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": review_content},
        ],
        temperature=0.1,
    )

    raw_output = response.choices[0].message.content

    # Parse rating from structured output
    rating = 5  # Safe default fallback
    clean_summary = raw_output

    if "FINAL_RATING:" in raw_output:
        parts = raw_output.split("FINAL_RATING:")
        clean_summary = parts[0].strip()
        try:
            rating = int("".join(filter(str.isdigit, parts[1])))
        except (ValueError, IndexError):
            rating = 5

    # Determine category bracket
    if 8 <= rating <= 10:
        category = "Good"
    elif 4 <= rating <= 7:
        category = "Average"
    else:
        category = "Bad"

    return {
        "summary": clean_summary,
        "rating": rating,
        "category": category,
    }
