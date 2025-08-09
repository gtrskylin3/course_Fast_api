from pydantic import BaseModel, Field

class CreateProduct(BaseModel):
    name: str
    description: str
    price: int
    image_url: str
    stock: int
    category: int


from typing import Optional
class CreateCategory(BaseModel):
    name: str
    parent_id: Optional[int]
