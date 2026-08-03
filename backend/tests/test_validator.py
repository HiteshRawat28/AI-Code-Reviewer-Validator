import pytest
from app.services.json_validator import parse_and_validate
from app.schemas.review_schema import ReviewResponse

def test_valid_json():
    raw = '''{
        "bugs": [{"category": "bug", "severity": "high", "description": "test", "line_number": 1}],
        "style_issues": [],
        "security_issues": []
    }'''
    result, error = parse_and_validate(raw)
    assert error is None
    assert isinstance(result, ReviewResponse)
    assert len(result.bugs) == 1
    assert result.bugs[0].category == "bug"

def test_valid_json_with_markdown_fences():
    raw = '''```json
    {
        "bugs": [],
        "style_issues": [],
        "security_issues": []
    }
    ```'''
    result, error = parse_and_validate(raw)
    assert error is None
    assert isinstance(result, ReviewResponse)

def test_malformed_json():
    raw = '''{ "bugs": [ '''
    result, error = parse_and_validate(raw)
    assert result is None
    assert "Failed to parse" in error

def test_invalid_schema_missing_fields():
    raw = '''{
        "bugs": [{"severity": "high"}]
    }'''
    result, error = parse_and_validate(raw)
    assert result is None
    assert "did not match the expected schema" in error

def test_invalid_schema_wrong_severity():
    raw = '''{
        "bugs": [{"category": "bug", "severity": "ultra", "description": "test"}],
        "style_issues": [],
        "security_issues": []
    }'''
    result, error = parse_and_validate(raw)
    assert result is None
    assert "did not match the expected schema" in error
