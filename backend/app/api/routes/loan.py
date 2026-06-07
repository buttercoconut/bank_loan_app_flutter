# routes/loan.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models.loan import LoanApplication, Customer, LoanProduct
from ..schemas import LoanApplicationCreate, LoanApplicationOut
from ...database import get_db

router = APIRouter(prefix="/loans", tags=["loans"])

@router.post("/apply", response_model=LoanApplicationOut)
def apply_loan(app: LoanApplicationCreate, db: Session = Depends(get_db)):
    # Basic validation
    customer = db.query(Customer).filter(Customer.id == app.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    product = db.query(LoanProduct).filter(LoanProduct.id == app.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Loan product not found")
    if app.amount > product.max_amount:
        raise HTTPException(status_code=400, detail="Amount exceeds product limit")
    # Simple credit check logic
    credit_score = 700  # placeholder, would call external service
    if credit_score < 600:
        status_str = "rejected"
    elif app.debt_ratio > 0.4:
        status_str = "rejected"
    else:
        status_str = "approved"
    loan = LoanApplication(
        customer_id=app.customer_id,
        product_id=app.product_id,
        amount=app.amount,
        income=app.income,
        debt_ratio=app.debt_ratio,
        status=status_str,
    )
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan

@router.get("/{loan_id}", response_model=LoanApplicationOut)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(LoanApplication).filter(LoanApplication.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan
