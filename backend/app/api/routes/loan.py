# app/api/routes/loan.py
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from typing import List

from app.api.models.loan import (
    LoanApplication,
    LoanApplicationCreate,
    LoanApplicationUpdate,
    LoanApplicationResponse,
    LoanStatusResponse,
)
from app.api.schemas import (
    LoanApplicationCreateSchema,
    LoanApplicationUpdateSchema,
    LoanApplicationResponseSchema,
    LoanStatusResponseSchema,
)

router = APIRouter()

# In-memory store for demo purposes
_db: List[LoanApplication] = []
_next_id = 1

# Simple credit decision logic

def evaluate_loan(app: LoanApplicationCreate) -> LoanStatusResponse:
    if app.credit_score < 600:
        return LoanStatusResponse(
            id=0,
            status="rejected",
            decision="credit_score_low",
            reason="Credit score below 600",
        )
    if app.debt_ratio > 0.4:
        return LoanStatusResponse(
            status="rejected",
            decision="high_debt_ratio",
            reason="Debt-to-income ratio exceeds 40%",
        )
    return LoanStatusResponse(
        id=0,
        status="approved",
        decision="eligible",
        reason=None,
    )

@router.post("/", response_model=LoanApplicationResponseSchema)
async def create_loan(
    payload: LoanApplicationCreateSchema,
):
    global _next_id
    app_create = LoanApplicationCreate(**payload.dict())
    status = evaluate_loan(app_create)
    if status.status == "rejected":
        raise HTTPException(status_code=400, detail=status.reason)
    # Create LoanApplication instance
    loan = LoanApplication(
        id=_next_id,
        customer=LoanApplicationCreate(customer_id=app_create.customer_id, name="", email="", phone="", ssn=""),
        product=LoanApplicationCreate(product_id=app_create.product_id, name="", interest_rate=0.0, max_amount=0.0, min_credit_score=0),
        amount=app_create.amount,
        income=app_create.income,
        debt_ratio=app_create.debt_ratio,
        credit_score=app_create.credit_score,
        status="pending",
        created_at=datetime.utcnow(),
        repayments=[],
    )
    _db.append(loan)
    _next_id += 1
    return LoanApplicationResponseSchema(
        id=loan.id,
        status=loan.status,
        amount=loan.amount,
        created_at=loan.created_at.isoformat(),
    )

@router.get("/", response_model=List[LoanApplicationResponseSchema])
async def list_loans():
    return [
        LoanApplicationResponseSchema(
            id=loan.id,
            status=loan.status,
            amount=loan.amount,
            created_at=loan.created_at.isoformat(),
        )
        for loan in _db
    ]

@router.get("/{loan_id}", response_model=LoanApplicationResponseSchema)
async def get_loan(loan_id: int):
    for loan in _db:
        if loan.id == loan_id:
            return LoanApplicationResponseSchema(
                id=loan.id,
                status=loan.status,
                amount=loan.amount,
                created_at=loan.created_at.isoformat(),
            )
    raise HTTPException(status_code=404, detail="Loan not found")

@router.put("/{loan_id}", response_model=LoanApplicationResponseSchema)
async def update_loan(loan_id: int, payload: LoanApplicationUpdateSchema):
    for loan in _db:
        if loan.id == loan_id:
            if payload.status:
                loan.status = payload.status
            if payload.amount:
                loan.amount = payload.amount
            return LoanApplicationResponseSchema(
                id=loan.id,
                status=loan.status,
                amount=loan.amount,
                created_at=loan.created_at.isoformat(),
            )
    raise HTTPException(status_code=404, detail="Loan not found")

@router.get("/{loan_id}/status", response_model=LoanStatusResponseSchema)
async def get_loan_status(loan_id: int):
    for loan in _db:
        if loan.id == loan_id:
            return LoanStatusResponseSchema(
                id=loan.id,
                status=loan.status,
                decision="",
                reason=None,
            )
    raise HTTPException(status_code=404, detail="Loan not found")
