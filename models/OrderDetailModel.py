from pydantic import BaseModel

class OrderDetailModel(BaseModel):
    id: int
    order_id: int
    product_id: int
    unit_price: int
    quantity: int