# schemas.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

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
    class Config:
        orm_mode = True

class LoanApplicationCreate(BaseModel):
    customer_id: int
    product_id: int
    amount: float
    income: float
    debt_ratio: float

class LoanApplicationOut(BaseModel):
    id: int
    customer_id: int
    product_id: int
    amount: float
    income: float
    debt_ratio: float
    status: str
    created_at: datetime
    class Config:
        orm_mode = True
