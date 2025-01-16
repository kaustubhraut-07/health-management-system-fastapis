from fastapi import APIRouter, HTTPException
from config.dbConnect import MongoDB
from models.doctor import doctor
from typing import List
from bson.objectid import ObjectId as objectId
from config.accesstoken import create_access_token
from passlib.context import CryptContext
from fastapi import Depends
from config.accesstoken import get_current_user

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/")
async def get_all_doctors(current_user: doctor = Depends(get_current_user)):
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
        hash_password = pwd_context.hash(doctor.password)
        doctor.password = hash_password
        result = await doctor_collection.insert_one(doctor.dict())
        return {"message": "Doctor created successfully", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/doctorlogin", response_model=dict)
async def doctor_login(doctor: doctor):
    try:
        
        doctor_collection = MongoDB.database["doctors"]

   
        db_doctor = await doctor_collection.find_one({"email": doctor.email})
        if not db_doctor:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        
        print(doctor.password, db_doctor["password"])
        if not pwd_context.verify(doctor.password, db_doctor["password"]):
            raise HTTPException(status_code=401, detail="Invalid email or password")

      
        token = create_access_token({"sub": db_doctor["email"]})
        return {"access_token": token, "token_type": "bearer"}
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