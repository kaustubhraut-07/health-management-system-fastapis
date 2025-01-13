from pymongo import MongoClient
from models.patient import Patient
from pydantic import BaseModel, Field
class doctor(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str
    mobileNo: str
    email: str
    address : str
    specility : str
    experience : str
    number_of_patient : [Patient]

    def __init__(self, name, mobileNo, email, address, specility, experience, number_of_patient):
        self.name = name
        self.mobileNo = mobileNo
        self.email = email
        self.address = address
        self.specility = specility
        self.experience = experience
        self.number_of_patient = number_of_patient

    def __str__(self):
        return f"Name: {self.name}, Mobile No: {self.mobileNo}, Email: {self.email}, Address: {self.address}, Specility: {self.specility}, Experience: {self.experience}, Number of patient: {self.number_of_patient}"
    

