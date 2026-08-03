from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    print("GET /health -> 200 OK")

def test_review_empty_code():
    response = client.post("/api/review", json={"code": "", "language": "python"})
    assert response.status_code == 422
    print(f"POST /api/review (empty code) -> {response.status_code} (Expected 422)")

def test_review_too_long():
    long_code = "x" * 50001
    response = client.post("/api/review", json={"code": long_code, "language": "python"})
    assert response.status_code == 413
    print(f"POST /api/review (code too long) -> {response.status_code} (Expected 413)")

def test_review_quota_error():
    # This should trigger the LLM call, go through the fallback loop, and finally return a 503
    # because the provided API key has insufficient quota.
    response = client.post("/api/review", json={"code": "def hello(): pass", "language": "python"})
    print(f"POST /api/review (LLM call) -> {response.status_code} (Expected 503 due to quota)")
    print("Response JSON:", json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_health()
    test_review_empty_code()
    test_review_too_long()
    test_review_quota_error()
    print("All endpoint tests finished!")
