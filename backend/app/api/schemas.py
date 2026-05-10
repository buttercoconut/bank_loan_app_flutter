from pydantic import BaseModel, Field
from datetime import datetime

class LoanApplicationCreate(BaseModel):
    customer_id: int
    customer_name: str
    product_id: int
    product_name: str
    interest_rate: float
    amount: float

class LoanApplicationResponse(BaseModel):
    id: int
    customer_id: int
    product_id: int
    amount: float
    status: str
    applied_at: datetime

    class Config:
        orm_mode = True
