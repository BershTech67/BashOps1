from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    date_of_birth = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    prescriptions = relationship("Prescription", back_populates="patient")

class Prescription(Base):
    __tablename__ = "prescriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    drug_name = Column(String, nullable=False)
    dosage = Column(String)
    frequency = Column(String)
    status = Column(String, default="active")
    prescribed_date = Column(DateTime(timezone=True), server_default=func.now())
    
    patient = relationship("Patient", back_populates="prescriptions")

class Drug(Base):
    __tablename__ = "drugs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    generic_name = Column(String)
    category = Column(String)
    in_stock = Column(Integer, default=0)
