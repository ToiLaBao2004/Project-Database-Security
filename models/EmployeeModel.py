from pydantic import BaseModel
from datetime import date
from typing import Optional
class EmployeeModel(BaseModel):
    id: Optional[int]=None
    name: str
    dateofbirth: date
    gender: str
    address: str
    phonenumber:str
    email: str
    username: str
    password: str
    emp_role: str
