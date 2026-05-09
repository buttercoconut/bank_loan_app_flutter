# app/api/schemas.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional
from enum import Enum

class LoanStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REPAID = "REPAID"

class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str

class CustomerOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str

    class Config:
        orm_mode = True

class LoanProductOut(BaseModel):
    id: int
    name: str
    interest_rate: float
    max_amount: float
    min_amount: float

    class Config:
        orm_mode = True

class LoanApplicationCreate(BaseModel):
    customer_id: int
    product_id: int
    amount: float
    term_months: int

class LoanApplicationOut(BaseModel):
    id: int
    customer: CustomerOut
    product: LoanProductOut
    amount: float
    term_months: int
    status: LoanStatus
    applied_at: datetime
    approved_at: Optional[datetime]

    class Config:
        orm_mode = True

class RepaymentCreate(BaseModel):
    application_id: int
    amount: float

class RepaymentOut(BaseModel):
    id: int
    application_id: int
    amount: float
    paid_at: datetime

    class Config:
        orm_mode = True
