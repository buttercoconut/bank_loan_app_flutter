# main.py
from fastapi import FastAPI
from .api.routes import loan
from .database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bank Loan Service API")

app.include_router(loan.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Bank Loan Service API"}
