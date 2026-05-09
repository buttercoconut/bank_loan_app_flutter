# app/api/routes/loan.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from ..models import database, loan as models
from ..schemas import (
    CustomerCreate,
    CustomerOut,
    LoanProductOut,
    LoanApplicationCreate,
    LoanApplicationOut,
    RepaymentCreate,
    RepaymentOut,
    LoanStatus,
)

router = APIRouter()

# Dependency to get DB session
async def get_db() -> AsyncSession:
    async with database.async_session() as session:
        yield session

# Helper: simple credit check logic
async def evaluate_loan(session: AsyncSession, application: models.LoanApplication) -> bool:
    # Dummy logic: approve if amount <= 50000 and term <= 60 months
    if application.amount <= 50000 and application.term_months <= 60:
        return True
    return False

@router.post("/applications", response_model=LoanApplicationOut)
async def create_application(app_in: LoanApplicationCreate, db: AsyncSession = Depends(get_db)):
    # Verify customer exists
    result = await db.execute(select(models.Customer).where(models.Customer.id == app_in.customer_id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Verify product exists
    result = await db.execute(select(models.LoanProduct).where(models.LoanProduct.id == app_in.product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Loan product not found")

    # Create application
    application = models.LoanApplication(
        customer_id=app_in.customer_id,
        product_id=app_in.product_id,
        amount=app_in.amount,
        term_months=app_in.term_months,
        status=models.LoanStatus.PENDING,
    )
    db.add(application)
    try:
        await db.commit()
        await db.refresh(application)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Integrity error")

    # Evaluate loan
    approved = await evaluate_loan(db, application)
    application.status = models.LoanStatus.APPROVED if approved else models.LoanStatus.REJECTED
    if approved:
        application.approved_at = datetime.utcnow()
    await db.commit()
    await db.refresh(application)

    return application

@router.get("/applications/{app_id}", response_model=LoanApplicationOut)
async def get_application(app_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.LoanApplication).where(models.LoanApplication.id == app_id))
    application = result.scalar_one_or_none()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application

@router.post("/repayments", response_model=RepaymentOut)
async def make_repayment(rep_in: RepaymentCreate, db: AsyncSession = Depends(get_db)):
    # Verify application exists and is approved
    result = await db.execute(select(models.LoanApplication).where(models.LoanApplication.id == rep_in.application_id))
    application = result.scalar_one_or_none()
    if not application:
        raise HTTPException(status_code=404, detail="Loan application not found")
    if application.status != models.LoanStatus.APPROVED:
        raise HTTPException(status_code=400, detail="Cannot repay a non-approved loan")

    repayment = models.Repayment(
        application_id=rep_in.application_id,
        amount=rep_in.amount,
    )
    db.add(repayment)
    await db.commit()
    await db.refresh(repayment)

    # Simple check if total repayments >= amount
    result = await db.execute(select(models.Repayment).where(models.Repayment.application_id == rep_in.application_id))
    repayments = result.scalars().all()
    total_paid = sum(r.amount for r in repayments)
    if total_paid >= application.amount:
        application.status = models.LoanStatus.REPAID
        await db.commit()

    return repayment

# Additional endpoints like list applications, list repayments can be added
