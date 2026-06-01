# app/api/models/loan.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    # For simplicity, store hashed password
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    applications = relationship("LoanApplication", back_populates="customer")

class LoanProduct(Base):
    __tablename__ = "loan_products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    interest_rate = Column(Float, nullable=False)
    max_amount = Column(Float, nullable=False)

class LoanApplication(Base):
    __tablename__ = "loan_applications"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    product_id = Column(Integer, ForeignKey("loan_products.id"))
    amount = Column(Float, nullable=False)
    income = Column(Float, nullable=False)
    debt_ratio = Column(Float, nullable=False)
    status = Column(String, default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="applications")
    product = relationship("LoanProduct")
