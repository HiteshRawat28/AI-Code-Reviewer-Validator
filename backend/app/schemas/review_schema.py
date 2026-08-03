from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class Issue(BaseModel):
    """
    Represents a single issue found in the code review.
    """
    category: Literal["bug", "style", "security"] = Field(
        ..., description="The type of issue found: bug, style, or security"
    )
    severity: Literal["low", "medium", "high", "critical"] = Field(
        ..., description="The severity level of the issue"
    )
    description: str = Field(
        ..., description="A clear, concise explanation of the issue"
    )
    line_number: Optional[int] = Field(
        None, description="The specific line number where the issue occurs, if applicable"
    )

class ReviewResponse(BaseModel):
    """
    The structured response containing all categorized issues from the code review.
    """
    bugs: List[Issue] = Field(
        default_factory=list, description="List of functional bugs or logic errors"
    )
    style_issues: List[Issue] = Field(
        default_factory=list, description="List of stylistic problems, naming conventions, etc."
    )
    security_issues: List[Issue] = Field(
        default_factory=list, description="List of potential vulnerabilities or unsafe practices"
    )

class ReviewRequest(BaseModel):
    """
    The request payload sent by the frontend containing the code to review.
    """
    code: str = Field(..., description="The raw code snippet to be reviewed")
    language: str = Field(..., description="The programming language of the snippet")
