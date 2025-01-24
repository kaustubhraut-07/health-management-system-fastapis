from pymongo import MongoClient
from pydantic import BaseModel
from typing import Optional
from pydantic import Field
from typing import List


class Appointment(BaseModel):
    appointment_day: Optional[str] = None
    appointment_time: Optional[str] = None
    appointment_status: Optional[str] = Field(default="pending")
    doctor_id: Optional[str] = None


class Patient(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")  
    name : str
    mobileNo : str
    email : str
    address  : Optional[str] = None
    description : str
    consult_to_doctor : Optional[str] = None
    appoints_data: List[Appointment] = Field(default=[])
   


 

    def __str__(self):
        return f"_id : {self._id}, Name: {self.name}, Mobile No: {self.mobileNo}, Address: {self.address}, Description: {self.description}, Consult to doctor: {self.consult_to_doctor}"
    
class Config:
     allow_population_by_field_name = True