from pymongo import MongoClient
from models.patient import Patient
from pydantic import BaseModel, Field
from typing import Optional
class doctor(BaseModel):
    id: Optional[str] = Field(alias="_id" , default=None)
    name: str
    mobileNo: str
    email: str
    address : str
    specility : str
    experience : str
    number_of_patient : list = Field(default=[], alias="number_of_patient") #patient_id : str



    def __str__(self):
        return f"_id : {self.id} ,Name: {self.name}, Mobile No: {self.mobileNo}, Email: {self.email}, Address: {self.address}, Specility: {self.specility}, Experience: {self.experience}, Number of patient: {self.number_of_patient}"
    

class Config:
    allow_population_by_field_name = True