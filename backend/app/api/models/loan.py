# models/loan.py
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class LoanApplication(Base):
    __tablename__ = "loan_applications"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, index=True)
    product_id = Column(Integer, index=True)
    amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    term_months = Column(Integer, nullable=False)
    status = Column(String, default="PENDING")
    created_at = Column(Date, default=None)
    # relationships
    repayments = relationship("Repayment", back_populates="loan")

class Repayment(Base):
    __tablename__ = "repayments"
    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loan_applications.id"))
    amount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=False)
    paid = Column(String, default="NO")
    loan = relationship("LoanApplication", back_populates="repayments")
