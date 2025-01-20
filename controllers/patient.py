from fastapi import APIRouter, HTTPException,File, UploadFile
from config.dbConnect import MongoDB
from config.mail import send_email_async , send_email_background
from models.patient import Patient
from typing import List
from bson.objectid import ObjectId as objectId
import json
from fastapi import BackgroundTasks
from pathlib import Path
import shutil
from fastapi_utilities import repeat_at
import datetime
from datetime import datetime, timedelta
import asyncio

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
        # if "_id" not in update_data or not update_data["_id"]:
        #     raise HTTPException(status_code=400, detail="Patient ID (_id) is required for updates")
        
        print(update_data , "update_data")
        patient_id = update_data['id'] 
        print(patient_id)
        result = await patient_collection.update_one({"_id": objectId(patient_id)}, {"$set": update_data})

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Patient not found")
        return {"message": "Patient updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    

@router.delete("/{patient_id}", response_model=dict)
async def delete_patient(patient_id: str):
    try:
        patient_collection = MongoDB.database["patients"]
        result = await patient_collection.delete_one({"_id": objectId(patient_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Patient not found")
        return {"message": "Patient deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/bookappointment", response_model=dict)
async def book_appointment(appointment: dict):
    try:
        patient_collection = MongoDB.database["patients"]

        await run_after_delay(Path("uploads"), days=10, delay_seconds=5)
        if not appointment.get('doctor_id') or not appointment.get('appointment_day') or not appointment.get('appointment_time'):
            raise HTTPException(status_code=400, detail="Doctor ID, Appointment Date, and Appointment Time are required")

        
        patient = await patient_collection.find_one({"_id": objectId(appointment['patient_id'])})
        # print(patient)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")

      
        email_to = patient.get('email')
        # print(email_to)
        if not email_to or '@' not in email_to:
            raise HTTPException(status_code=400, detail="Patient email not found or invalid")

        
        result = await patient_collection.update_one(
            {"_id": objectId(appointment['patient_id'])},
            {"$push": {"appoints_data": appointment}}
        )
        # print(result)

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Failed to book appointment")

        
        email_subject = "Appointment Confirmation"
        # email_body = f"Your appointment with Doctor has been successfully booked for {appointment['appointment_day']} at {appointment['appointment_time']}."
        email_body= f"""
        <html>
        <body style="margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, Helvetica, sans-serif;">
        <div style="width: 100%; background: #efefef; border-radius: 10px; padding: 10px;">
          <div style="margin: 0 auto; width: 90%; text-align: center;">
            <h1 style="background-color: rgba(0, 53, 102, 1); padding: 5px 10px; border-radius: 5px; color: white;">Appointment Confirmation</h1>
            <div style="margin: 30px auto; background: white; width: 40%; border-radius: 10px; padding: 50px; text-align: center;">
              <h3 style="margin-bottom: 100px; font-size: 24px;">{patient.get('name')}!</h3>
              <p style="margin-bottom: 30px;">Your appointment with the doctor has been successfully booked.</p>
              <p style="margin-bottom: 30px;"><strong>Appointment Date:</strong> {appointment['appointment_day']}</p>
              <p style="margin-bottom: 30px;"><strong>Appointment Time:</strong> {appointment['appointment_time']}</p>
             
            </div>
          </div>
        </div>
        </body>
        </html>
        """


        
        await send_email_async(subject=email_subject, email_to=email_to, body=email_body)

        return {"message": "Appointment booked successfully and confirmation email sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# update appointment status of patinet
@router.patch("/updateappointment_status", response_model=dict)
async def update_appointment(appointment: dict):
    try:
        patient_collection = MongoDB.database["patients"]

        result = await patient_collection.update_one(
            {"_id": objectId(appointment['patient_id'])},  
            {
                "$set": {
                    "appoints_data.$[elem].appointment_status": appointment['appointment_status']  
                }
            },
            array_filters=[{"elem.doctor_id": appointment['doctor_id']}], 
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Patient not found")
        return {"message": "Appointment status updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@router.post("/upload_reports")
async def upload_reports(patient_id: str, files: list[UploadFile], background_tasks: BackgroundTasks):
    try:
        patient_uploads_dir = Path("uploads") / patient_id
        patient_uploads_dir.mkdir(parents=True, exist_ok=True)
        

        file_paths = []
        for file in files:
            file_path = patient_uploads_dir / file.filename
            file_paths.append(str(file_path))

            file_content = await file.read()
            
            background_tasks.add_task(save_file, file_content, file_path)

        return {"message": "Files uploaded successfully", "file_paths": file_paths}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def save_file(file_content: bytes, destination: Path):
    with destination.open("wb") as buffer:
        buffer.write(file_content)

@repeat_at(cron="0 12 * * *") 
def delete_old_files(folder_path: Path = Path("uploads"), days: int = 0.5):
    """
    Deletes files older than a specified number of days.
    
    Args:
        folder_path (Path): Path to the folder containing files to delete.
        days (int): The age of files (in days) to delete.
    """
    try:
        cutoff_date = datetime.now() - timedelta(days=days)

        for file_path in folder_path.iterdir():
            if file_path.is_file():
                file_modified_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_modified_time < cutoff_date:
                    file_path.unlink()
                    print(f"Deleted: {file_path}")
                else:
                    print(f"File not old enough: {file_path}")
    except Exception as e:
        print(f"Error occurred: {e}")


async def run_after_delay(folder_path: Path, days: int = 10, delay_seconds: int = 30):
    """
    Run the delete_old_files function after a delay.
    
    Args:
        folder_path (Path): Path to the folder containing files to delete.
        days (int): The age of files (in days) to delete.
        delay_seconds (int): Delay in seconds before running the function.
    """
    print(f"Current Time: {datetime.now()}")
    print(f"Waiting for {delay_seconds} seconds to run the function...")
    await asyncio.sleep(delay_seconds)
    delete_old_files(folder_path, days)
    print(f"Function executed at: {datetime.now()}")


