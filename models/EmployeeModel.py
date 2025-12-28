from pydantic import BaseModel
from datetime import date
from enum import StrEnum

class ROLE(StrEnum):
    MANAGER = "MGR"
    EMPLOYEE = "EMP" 

class EmployeeModel(BaseModel):
    id: int
    name: str
    date_of_birth: date
    gender: str
    address: str
    phone_number:str
    email: str
    username: str
    role: ROLE
