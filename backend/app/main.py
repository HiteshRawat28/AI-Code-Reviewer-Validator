from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.review import router as review_router

app = FastAPI(title="AI Code Reviewer API")

# Configure CORS for local development and deployed frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
