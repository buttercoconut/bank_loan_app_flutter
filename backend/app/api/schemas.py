# schemas.py
from pydantic import BaseModel, Field
from datetime import date

class LoanApplicationCreate(BaseModel):
    customer_id: int
    product_id: int
    amount: float
    interest_rate: float
    term_months: int
    created_at: date = Field(default_factory=date.today)

class LoanApplicationResponse(LoanApplicationCreate):
    id: int
    status: str
    created_at: date

    class Config:
        orm_mode = True
