from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    # relationships
    applications = relationship("LoanApplication", back_populates="customer")

class LoanProduct(Base):
    __tablename__ = "loan_products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    interest_rate = Column(Float, nullable=False)
    # relationships
    applications = relationship("LoanApplication", back_populates="product")

class LoanApplication(Base):
    __tablename__ = "loan_applications"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    product_id = Column(Integer, ForeignKey("loan_products.id"))
    amount = Column(Float, nullable=False)
    status = Column(String, default="PENDING")
    applied_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="applications")
    product = relationship("LoanProduct", back_populates="applications")
