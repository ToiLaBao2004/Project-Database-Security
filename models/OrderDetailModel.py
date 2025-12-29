from pydantic import BaseModel
from typing import Optional

class OrderDetailModel(BaseModel):
    id: Optional[int]=None
    order_id: int
    product_id: int
    unit_price: int
    quantity: int