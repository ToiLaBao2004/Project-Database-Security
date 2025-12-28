from pydantic import BaseModel
class ProductModel(BaseModel):
    id: int
    name: str
    image: str
    unit_price: int
    stock_quantity: int
    category_id: int
    brand_id: int
    active: bool