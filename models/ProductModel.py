from pydantic import BaseModel
from typing import Optional
class ProductModel(BaseModel):
    id: Optional[int]=None
    name: str
    image: str
    unit_price: int
    stock_quantity: int
    category_id: int
    brand_id: int
    active: bool