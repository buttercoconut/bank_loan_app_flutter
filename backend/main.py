# main.py
from fastapi import FastAPI
from app.api.routes import loan
from app.api.models import database

app = FastAPI(title="Bank Loan API")

# Include routers
app.include_router(loan.router, prefix="/api/loan", tags=["loan"])

# Startup event to create tables
@app.on_event("startup")
async def startup():
    await database.init_models()

# Shutdown event to close DB
@app.on_event("shutdown")
async def shutdown():
    await database.close()
