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
        # print(users)
        
        # Convert ObjectId to string
        for user in users:
            user["_id"] = str(user["_id"])
            print(user)
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


@router.patch("/", response_model=dict)
async def update_patient(patient: Patient):
    try:
        patient_collection = MongoDB.database["patients"]
        # print(patient_collection)
        
        update_data = patient.dict()
        # print(update_data , "update_data")
        if "_id" not in update_data or not update_data["_id"]:
            raise HTTPException(status_code=400, detail="Patient ID (_id) is required for updates")

        patient_id = update_data.pop("_id")  
        print(patient_id)
        result = await patient_collection.update_one({"_id": patient_id}, {"$set": update_data})

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Patient not found")
        return {"message": "Patient updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    

@router.delete("/{patient_id}", response_model=dict)
async def delete_patient(patient_id: str):
    try:
        patient_collection = MongoDB.database["patients"]
        result = await patient_collection.delete_one({"_id": patient_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Patient not found")
        return {"message": "Patient deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    