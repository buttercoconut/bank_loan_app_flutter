# loan.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.loan import LoanApplication, Loan
from ..schemas import LoanApplicationCreate, LoanApplicationResponse
from ...database import get_db

router = APIRouter(prefix="/loans", tags=["loans"])

@router.post("/apply", response_model=LoanApplicationResponse)
def apply_loan(loan_in: LoanApplicationCreate, db: Session = Depends(get_db)):
    # Basic validation and creation logic
    loan = LoanApplication(**loan_in.dict())
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan

@router.get("/{loan_id}", response_model=LoanApplicationResponse)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(LoanApplication).filter(LoanApplication.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan
