from pymongo import MongoClient
from pydantic import BaseModel
from typing import Optional
class Patient(BaseModel):
    name : str
    mobileNo : str
    address  : Optional[str] = None
    description : str
    consult_to_doctor : str

    

    def __str__(self):
        return f"Name: {self.name}, Mobile No: {self.mobileNo}, Address: {self.address}, Description: {self.description}, Consult to doctor: {self.consult_to_doctor}"
    
