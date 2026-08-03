import logging
import groq
from app.core.config import settings

logger = logging.getLogger(__name__)

# Initialize the Groq Async Client. It will safely remain None if the key is missing or default.
client = None
if settings.GROQ_API_KEY and settings.GROQ_API_KEY != "your_groq_api_key_here":
    client = groq.AsyncGroq(api_key=settings.GROQ_API_KEY)

# Order of models to try. If one hits a quota error, it falls back to the next.
MODELS_TO_TRY = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "gemma2-9b-it"
]

async def generate_review(prompt: str) -> str:
    """
    Sends the structured prompt to the Groq API and returns the raw text response.
    Implements a fallback mechanism across multiple models to handle 429 Quota errors.
    Catches API errors and raises a clear, user-facing error if all fallbacks fail.
    """
    if not client:
        raise ValueError("Review service is temporarily unavailable — missing API key.")

    last_exception = None

    for model_name in MODELS_TO_TRY:
        try:
            logger.info(f"Attempting LLM call with model: {model_name}")
            response = await client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content

        except groq.RateLimitError as e:
            # 429 errors usually mean insufficient quota or rate limits.
            logger.warning(f"RateLimit/Quota error with {model_name}: {e}. Falling back to next model...")
            last_exception = e
            continue
            
        except groq.APIError as e:
            logger.error(f"Groq API Error with {model_name}: {e}")
            # If it's a general API error, we can still try to fallback
            last_exception = e
            continue
            
        except Exception as e:
            logger.error(f"Unexpected error calling LLM with {model_name}: {e}")
            last_exception = e
            continue

    # If we exhausted the list and have an exception
    logger.error(f"All model fallbacks exhausted. Last error: {last_exception}")
    raise ValueError("Review service is temporarily unavailable — please try again.")
