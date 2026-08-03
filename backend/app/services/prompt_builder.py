import json

def build_review_prompt(code: str, language: str) -> str:
    """
    Builds the structured prompt for the Gemini LLM to review the provided code snippet.
    
    The prompt is specifically engineered to:
    1. Force a strict JSON output matching our Pydantic schema.
    2. Prevent the LLM from wrapping the JSON in markdown code blocks (e.g., ```json ... ```) 
       which makes parsing easier.
    3. Ensure issues are correctly categorized into bugs, style_issues, and security_issues.
    """
    
    # We define the schema structure explicitly in the prompt so the LLM understands 
    # the exact keys and valid values it must return. We use JSON stringification 
    # of a template to make it unambiguous.
    schema_template = {
        "bugs": [
            {
                "category": "bug",
                "severity": "<low|medium|high|critical>",
                "description": "<string explaining the issue>",
                "line_number": "<integer or null>"
            }
        ],
        "style_issues": [
            {
                "category": "style",
                "severity": "<low|medium|high|critical>",
                "description": "<string explaining the issue>",
                "line_number": "<integer or null>"
            }
        ],
        "security_issues": [
            {
                "category": "security",
                "severity": "<low|medium|high|critical>",
                "description": "<string explaining the issue>",
                "line_number": "<integer or null>"
            }
        ]
    }

    prompt = f"""You are an expert, eagle-eyed senior software engineer and security auditor reviewing a code snippet.

Please review the following {language} code snippet. 

CODE TO REVIEW:
```
{code}
```

INSTRUCTIONS:
1. Identify any functional bugs or logic errors.
2. Identify any stylistic problems, bad practices, or naming convention violations.
3. Identify any potential security vulnerabilities or unsafe practices.
4. If no issues are found in a category, return an empty list for that category.

OUTPUT FORMAT REQUIREMENTS:
You MUST return your entire response as a single, valid JSON object. 
Do NOT wrap the JSON in markdown formatting or code blocks (do not use ```json or ```). 
Do NOT include any conversational text, introductions, or conclusions. Only output the raw JSON object.

The JSON object MUST perfectly match this exact schema structure:
{json.dumps(schema_template, indent=2)}

Begin your JSON output now:
"""
    return prompt
