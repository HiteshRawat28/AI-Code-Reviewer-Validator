from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.rate_limit import limiter
from app.routes.review import router as review_router

app = FastAPI(title="AI Code Reviewer API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS for deployed frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ai-code-reviewer-validator.vercel.app", "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(review_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the AI Code Reviewer API!",
        "health_check": "/health",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}
