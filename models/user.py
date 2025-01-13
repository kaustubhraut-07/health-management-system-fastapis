from pymongo import MongoClient

class User:
    name : str
    mobileNo : str
    address : str
    description : str
    consult_to_doctor : str

    def __init__(self, name, mobileNo, address, description, consult_to_doctor):
        self.name = name
        self.mobileNo = mobileNo
        self.address = address
        self.description = description
        self.consult_to_doctor = consult_to_doctor

    def __str__(self):
        return f"Name: {self.name}, Mobile No: {self.mobileNo}, Address: {self.address}, Description: {self.description}, Consult to doctor: {self.consult_to_doctor}"
    
