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

class CreateUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str

class CreateReviewWithRating(BaseModel):
    product_id: int
    comment: str = Field(max_length=200, description='Текст отзыва')
    grade: int = Field(gt=0, le=5, description='Оценка от 1 до 5')
