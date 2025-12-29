from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
class OrderModel(BaseModel):
    id: Optional[int]=None
    cus_id: int
    emp_id: int
    order_date_time: datetime=Field(default_factory=datetime.now)