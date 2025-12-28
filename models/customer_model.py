from pydantic import BaseModel
from datetime import date
class CustomerModel(BaseModel):
    id: int
    name: str
    phone_number: str
    email: str
    date_of_birth: date
    gender: bool
    