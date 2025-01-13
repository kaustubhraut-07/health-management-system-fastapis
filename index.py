# main.py
from fastapi import FastAPI
from config.dbConnect import MongoDB
from dotenv import load_dotenv
import os
from controllers.patient import router as patients_router

app = FastAPI()

load_dotenv(".env")

DB_URI = os.getenv("MONGO_URI")
print(DB_URI)
DB_NAME = "Management"

@app.on_event("startup")
async def startup_event():
    await MongoDB.connect(DB_URI, DB_NAME)

@app.on_event("shutdown")
async def shutdown_event():
    await MongoDB.disconnect()

@app.get("/")
async def root():
    return {"message": "FastAPI + MongoDB Example"}

@app.get("/users")
async def get_users():
    users_collection = MongoDB.database["users"]
    users = await users_collection.find().to_list(100) 
    return users


app.include_router(patients_router, prefix="/patients", tags=["patients"])