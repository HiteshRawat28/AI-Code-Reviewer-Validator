import json
import re
import logging
from typing import Optional, Tuple
from pydantic import ValidationError
from app.schemas.review_schema import ReviewResponse

logger = logging.getLogger(__name__)

def parse_and_validate(raw_text: str) -> Tuple[Optional[ReviewResponse], Optional[str]]:
    """
    Strips markdown code fences, parses the JSON, and validates against the ReviewResponse schema.
    Returns a tuple of (ReviewResponse, None) on success.
    Returns (None, error_message) on failure.
    """
    # 1. Strip markdown fences if the LLM ignored instructions
    # Often LLMs return ```json\n{...}\n```
    cleaned_text = raw_text.strip()
    
    # Remove leading ```json or ``` 
    cleaned_text = re.sub(r"^```(?:json)?\s*", "", cleaned_text, flags=re.IGNORECASE)
    # Remove trailing ```
    cleaned_text = re.sub(r"\s*```$", "", cleaned_text)
    
    cleaned_text = cleaned_text.strip()
    
    # 2. Attempt JSON parsing
    try:
        parsed_dict = json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing failed: {e}")
        logger.debug(f"Raw text was: {raw_text}")
        return None, "Failed to parse the LLM response as valid JSON."
        
    # 3. Attempt Pydantic validation
    try:
        validated_response = ReviewResponse(**parsed_dict)
        return validated_response, None
    except ValidationError as e:
        logger.error(f"Schema validation failed: {e}")
        return None, "The LLM response did not match the expected schema format."
