# app/api/models/loan.py
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class Customer(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    ssn: str = Field(..., alias="social_security_number")

class LoanProduct(BaseModel):
    id: int
    name: str
    interest_rate: float
    max_amount: float
    min_credit_score: int

class RepaymentInfo(BaseModel):
    id: int
    loan_application_id: int
    due_date: datetime
    amount: float
    paid: bool

class LoanApplication(BaseModel):
    id: int
    customer: Customer
    product: LoanProduct
    amount: float
    income: float
    debt_ratio: float
    credit_score: int
    status: str
    created_at: datetime
    repayments: List[RepaymentInfo] = []

# DTOs for requests
class LoanApplicationCreate(BaseModel):
    customer_id: int
    product_id: int
    amount: float
    income: float
    debt_ratio: float
    credit_score: int

class LoanApplicationUpdate(BaseModel):
    status: Optional[str] = None
    amount: Optional[float] = None

class LoanApplicationResponse(BaseModel):
    id: int
    status: str
    amount: float
    created_at: datetime

class LoanStatusResponse(BaseModel):
    id: int
    status: str
    decision: str
    reason: Optional[str] = None
