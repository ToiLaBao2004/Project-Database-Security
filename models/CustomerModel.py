from pydantic import BaseModel
from datetime import date
from typing import Optional
class CustomerModel(BaseModel):
    id: Optional[int]=None
    name: str
    phonenumber: str
    email: Optional[str]=None
    dateofbirth: Optional[date]=None
    gender: Optional[bool]=None
    