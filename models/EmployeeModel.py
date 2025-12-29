from pydantic import BaseModel
from datetime import date

class EmployeeModel(BaseModel):
    id: int
    name: str
    dateofbirth: date
    gender: str
    address: str
    phonenumber:str
    email: str
    username: str
    emp_role: str
