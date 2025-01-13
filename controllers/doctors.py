from fastapi import APIRouter, HTTPException
from config.dbConnect import MongoDB
from models.doctor import doctor
from typing import List
from bson.objectid import ObjectId as objectId


router = APIRouter()


@router.get("/")
async def get_all_doctors():
    try:
        doctor_collection = MongoDB.database["doctors"]
        doctors = await doctor_collection.find().to_list(100)
        for doctor in doctors:
            doctor["_id"] = str(doctor["_id"])


       
        return doctors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/", response_model=dict)
async def create_doctor(doctor: doctor):
    try:
        doctor_collection = MongoDB.database["doctors"]
        result = await doctor_collection.insert_one(doctor.dict())
        return {"message": "Doctor created successfully", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.patch("/", response_model=dict)
async def update_doctor(doctor: doctor):
    try:
        doctor_collection = MongoDB.database["doctors"]
        result = await doctor_collection.update_one({"_id": objectId(doctor.id)}, {"$set": doctor.dict()})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return {"message": "Doctor updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.delete("/{doctor_id}", response_model=dict)
async def delete_doctor(doctor_id: str):
    try:
        doctor_collection = MongoDB.database["doctors"]
        result = await doctor_collection.delete_one({"_id": objectId(doctor_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return {"message": "Doctor deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))