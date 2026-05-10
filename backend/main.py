"""Main entry point for the FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import loan

app = FastAPI(title="Bank Loan Service API", version="1.0.0")

# CORS settings for Flutter mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(loan.router, prefix="/api/loan", tags=["Loan"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}
