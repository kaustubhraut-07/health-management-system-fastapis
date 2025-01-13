from pymongo import MongoClient
from pydantic import BaseModel
from typing import Optional
from pydantic import Field
class Patient(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")  #
    name : str
    mobileNo : str
    address  : Optional[str] = None
    description : str
    consult_to_doctor : str

 

    def __str__(self):
        return f"_id : {self._id}, Name: {self.name}, Mobile No: {self.mobileNo}, Address: {self.address}, Description: {self.description}, Consult to doctor: {self.consult_to_doctor}"
    
class Config:
     allow_population_by_field_name = True