# main.py
from fastapi import FastAPI
from app.api.routes import loan
from app.database import engine, Base

app = FastAPI(title="Bank Loan API")

# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(loan.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Bank Loan API"}
