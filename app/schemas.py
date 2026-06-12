from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class PrescriptionUpload(BaseModel):
    patient_id: int
    raw_text: Optional[str] = None
    drug_name: str
    dosage: str
    frequency: str

class PrescriptionResponse(PrescriptionUpload):
    id: int
    status: str
    prescribed_date: datetime
    
    class Config:
        from_attributes = True

class InteractionCheckRequest(BaseModel):
    medications: List[str]

class InteractionResponse(BaseModel):
    severity: str
    description: str
    recommendations: str

class InventoryResponse(BaseModel):
    drug_name: str
    available: bool
    stock_count: int
    alternatives: List[str]
