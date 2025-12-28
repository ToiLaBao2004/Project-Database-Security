from pydantic import BaseModel, Field
from datetime import datetime
class OrderModel(BaseModel):
    id: int
    cus_id: int
    emp_id: int
    order_date_time: datetime=Field(default_factory=datetime.now)