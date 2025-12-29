from pydantic import BaseModel
from datetime import date
from typing import Optional

class EmployeeModel(BaseModel):
    id: Optional[int]=None
    name: Optional[str]=None
    dateofbirth: Optional[date]=None
    gender: Optional[bool]=None
    address: str 
    phonenumber:str 
    email: str
    username: Optional[str]=None
    password: Optional[str]=None
    emp_role: Optional[str]=None
