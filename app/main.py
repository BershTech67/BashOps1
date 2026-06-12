from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from .database import get_db, engine, Base
from . import models, schemas
from .services.drug_interaction_checker import check_interactions_ai

app = FastAPI(
    title="Ironsail Prescription Intelligence API",
    description="20% Prototype demonstrating AI-powered drug interaction and prescription verification.",
    version="1.0.0"
)

# 1. Prescription Upload Endpoint
@app.post("/api/v1/prescriptions/upload", response_model=schemas.PrescriptionResponse, status_code=status.HTTP_201_CREATED)
async def upload_prescription(prescription: schemas.PrescriptionUpload, db: AsyncSession = Depends(get_db)):
    # Validate patient exists
    result = await db.execute(select(models.Patient).where(models.Patient.id == prescription.patient_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Patient not found")

    new_rx = models.Prescription(
        patient_id=prescription.patient_id,
        drug_name=prescription.drug_name,
        dosage=prescription.dosage,
        frequency=prescription.frequency
    )
    db.add(new_rx)
    await db.commit()
    await db.refresh(new_rx)
    return new_rx

# 2. Drug Interaction Checker (AI-Powered)
@app.post("/api/v1/prescriptions/check-interactions", response_model=schemas.InteractionResponse)
async def check_drug_interactions(request: schemas.InteractionCheckRequest):
    if len(request.medications) < 2:
         return {"severity": "none", "description": "Not enough medications to form an interaction.", "recommendations": "N/A"}
    
    interaction_data = await check_interactions_ai(request.medications)
    return interaction_data

# 3. Patient Medication History
@app.get("/api/v1/patients/{patient_id}/medications", response_model=List[schemas.PrescriptionResponse])
async def get_patient_medications(patient_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Prescription).where(models.Prescription.patient_id == patient_id))
    medications = result.scalars().all()
    if not medications:
        raise HTTPException(status_code=404, detail="No medications found for this patient")
    return medications

# 4. Pharmacy Inventory Check (Mock)
@app.get("/api/v1/drugs/{drug_name}/availability", response_model=schemas.InventoryResponse)
async def check_inventory(drug_name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Drug).where(models.Drug.name.ilike(f"%{drug_name}%")))
    drug = result.scalar_one_or_none()
    
    if not drug:
        return schemas.InventoryResponse(
            drug_name=drug_name, available=False, stock_count=0, alternatives=["Generic Alternative A"]
        )
        
    return schemas.InventoryResponse(
        drug_name=drug.name, 
        available=drug.in_stock > 0, 
        stock_count=drug.in_stock, 
        alternatives=[drug.generic_name] if drug.generic_name else []
    )
