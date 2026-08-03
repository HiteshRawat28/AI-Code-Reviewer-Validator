from fastapi import APIRouter, HTTPException, status
from app.schemas.review_schema import ReviewRequest, ReviewResponse
from app.services.review_service import generate_and_validate_review

router = APIRouter(prefix="/api", tags=["Review"])

@router.post("/review", response_model=ReviewResponse)
async def create_review(request: ReviewRequest):
    """
    Accepts a code snippet, validates it, and generates an AI-powered code review.
    """
    # 1. Edge Case: Empty code
    if not request.code or not request.code.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Code snippet cannot be empty."
        )
    
    # 2. Edge Case: Code too long
    # We set a reasonable limit to prevent context window overflow or abuse (e.g., 50k characters)
    if len(request.code) > 50000:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Code snippet is too large. Please submit a smaller snippet."
        )

    # 3. Process the review
    try:
        review_result = await generate_and_validate_review(request.code, request.language)
        return review_result
    except ValueError as e:
        # Expected errors (API quota, parsing failures after retry)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )
    except Exception as e:
        # Unexpected crashes
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during review generation."
        )
