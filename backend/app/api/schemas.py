# app/api/schemas.py
from pydantic import BaseModel
from typing import List

class LoanApplicationCreateSchema(BaseModel):
    customer_id: int
    product_id: int
    amount: float
    income: float
    debt_ratio: float
    credit_score: int

class LoanApplicationUpdateSchema(BaseModel):
    status: str
    amount: float

class LoanApplicationResponseSchema(BaseModel):
    id: int
    status: str
    amount: float
    created_at: str

class LoanStatusResponseSchema(BaseModel):
    id: int
    status: str
    decision: str
    reason: str | None = None
