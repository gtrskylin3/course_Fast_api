from fastapi import FastAPI
from app.routers.category import router as category
from app.routers.products import router as products
from app.models.category import Category
from app.models.products import Product
from sqlalchemy.schema import CreateTable

print(CreateTable(Category.__table__))
print(CreateTable(Product.__table__))
app = FastAPI()



@app.get("/")
async def welcome() -> dict:
    return {"message": "My e-commerce app"}

app.include_router(category)
app.include_router(products)
