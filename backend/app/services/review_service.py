import logging
from app.services.prompt_builder import build_review_prompt
from app.services.llm_client import generate_review
from app.services.json_validator import parse_and_validate
from app.schemas.review_schema import ReviewResponse

logger = logging.getLogger(__name__)

async def generate_and_validate_review(code: str, language: str) -> ReviewResponse:
    """
    Coordinates building the prompt, calling the LLM, and validating the output.
    Implements a retry-once logic if the LLM fails to return valid JSON.
    """
    prompt = build_review_prompt(code, language)
    
    # Try 1
    raw_response = await generate_review(prompt)
    validated_data, error_msg = parse_and_validate(raw_response)
    
    if validated_data:
        return validated_data
        
    logger.warning(f"Initial LLM parse failed: {error_msg}. Retrying once with stricter prompt.")
    
    # Try 2 (Retry)
    retry_prompt = prompt + "\n\nCRITICAL WARNING: Your previous response was invalid. You MUST output ONLY raw JSON. NO MARKDOWN. NO BACKTICKS. NO CONVERSATION."
    
    retry_raw_response = await generate_review(retry_prompt)
    retry_validated_data, retry_error_msg = parse_and_validate(retry_raw_response)
    
    if retry_validated_data:
        return retry_validated_data
        
    logger.error(f"Retry LLM parse failed: {retry_error_msg}")
    raise ValueError(f"Failed to generate a valid code review format: {retry_error_msg}")
