# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.loan import router as loan_router

app = FastAPI(title="Bank Loan API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(loan_router, prefix="/api/loans", tags=["loans"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}
