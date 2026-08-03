import asyncio
import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
from app.services.llm_client import generate_review
from app.services.prompt_builder import build_review_prompt

sample_code = """
def greet(name):
    print("Hello " + name)
"""

async def main():
    prompt = build_review_prompt(code=sample_code, language="Python")
    print("Sending prompt to Groq...\n")
    
    try:
        result = await generate_review(prompt)
        print("\n--- OPENAI RESPONSE ---")
        print(result)
        print("-----------------------")
    except ValueError as e:
        print(f"\nCaught expected error (likely missing API key): {e}")
        print("To test for real, update backend/.env with a valid OPENAI_API_KEY.")

if __name__ == "__main__":
    asyncio.run(main())
