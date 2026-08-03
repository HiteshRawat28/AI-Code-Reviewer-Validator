from app.services.prompt_builder import build_review_prompt

sample_code = """
def calculate_total(prices):
    total = 0
    for i in range(len(prices)):
        total += prices[i]
    # TODO: Add tax calculation
    return total

def execute_query(user_id):
    query = "SELECT * FROM users WHERE id = " + str(user_id)
    # execute(query)
"""

prompt = build_review_prompt(code=sample_code, language="Python")

print("--- GENERATED PROMPT ---")
print(prompt)
print("------------------------")
print("\nTo manually test this, copy the above prompt and paste it into Google AI Studio (https://aistudio.google.com/app/prompts/new_chat).")
