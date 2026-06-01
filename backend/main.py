# main.py
from fastapi import FastAPI
from app.api.routes import loan
from app.database import engine, Base

app = FastAPI(title="Bank Loan Service API")

# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(loan.router, prefix="/api/loan", tags=["loan"])
