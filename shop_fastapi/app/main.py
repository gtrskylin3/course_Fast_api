from fastapi import FastAPI
from app.routers.category import router as category
from app.routers.products import router as products

app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return {"message": "My e-commerce app"}

app.include_router(category)
app.include_router(products)
