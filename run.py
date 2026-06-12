import uvicorn
import asyncio
from app.database import engine, Base
from app import models

async def init_db():
    async with engine.begin() as conn:
        # For prototype: Drop and recreate to ensure clean schema
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    # Seed Data
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker
    
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        # Seed Patient
        patient = models.Patient(name="John Doe", email="john@example.com", date_of_birth="1986-01-01")
        session.add(patient)
        
        # Seed Drugs
        drugs = [
            models.Drug(name="Lisinopril", generic_name="Prinivil", category="ACE Inhibitor", in_stock=150),
            models.Drug(name="Metformin", generic_name="Glucophage", category="Biguanide", in_stock=500),
            models.Drug(name="Warfarin", generic_name="Coumadin", category="Anticoagulant", in_stock=45),
            models.Drug(name="Aspirin", generic_name="Acetylsalicylic acid", category="NSAID", in_stock=1000)
        ]
        session.add_all(drugs)
        await session.commit()
        print("Database initialized and seeded successfully.")

if __name__ == "__main__":
    asyncio.run(init_db())
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
