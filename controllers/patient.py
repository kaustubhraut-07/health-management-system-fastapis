from fastapi import APIRouter, HTTPException
from config.dbConnect import MongoDB
from models.patient import Patient
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Patient])
async def get_all_patients():
    try:
        patient_collection = MongoDB.database["patients"]
        users = await patient_collection.find().to_list(100)
        
        # Convert ObjectId to string
        for user in users:
            user["_id"] = str(user["_id"])
        
        return [Patient(**user) for user in users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=dict)
async def create_patient(patient: Patient):
    try:
        patient_collection = MongoDB.database["patients"]
        result = await patient_collection.insert_one(patient.dict())
        return {"message": "Patient created successfully", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
