from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.api.schemas import LoanApplicationCreate, LoanApplicationResponse
from app.api.models import LoanApplication, Customer, LoanProduct
from app.database import get_db

router = APIRouter()

# Dummy in‑memory store for demo purposes
# In production use a real database via SQLAlchemy

@router.post("/apply", response_model=LoanApplicationResponse)
async def apply_loan(
    loan: LoanApplicationCreate,
    db: Session = Depends(get_db),
):
    # Basic validation
    if loan.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Loan amount must be positive",
        )
    # Create customer if not exists
    customer = db.query(Customer).filter_by(id=loan.customer_id).first()
    if not customer:
        customer = Customer(id=loan.customer_id, name=loan.customer_name)
        db.add(customer)
        db.commit()
        db.refresh(customer)
    # Create loan product if not exists
    product = db.query(LoanProduct).filter_by(id=loan.product_id).first()
    if not product:
        product = LoanProduct(id=loan.product_id, name=loan.product_name, interest_rate=loan.interest_rate)
        db.add(product)
        db.commit()
        db.refresh(product)
    # Create loan application
    application = LoanApplication(
        customer_id=customer.id,
        product_id=product.id,
        amount=loan.amount,
        status="PENDING",
        applied_at=datetime.utcnow(),
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return LoanApplicationResponse(
        id=application.id,
        customer_id=customer.id,
        product_id=product.id,
        amount=application.amount,
        status=application.status,
        applied_at=application.applied_at,
    )

@router.get("/status/{application_id}", response_model=LoanApplicationResponse)
async def get_status(application_id: int, db: Session = Depends(get_db)):
    application = db.query(LoanApplication).filter_by(id=application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return LoanApplicationResponse(
        id=application.id,
        customer_id=application.customer_id,
        product_id=application.product_id,
        amount=application.amount,
        status=application.status,
        applied_at=application.applied_at,
    )
