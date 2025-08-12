from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from app.routers.category import router as category
from app.routers.products import router as products
from app.routers.auth import router as auth
from app.routers.permission import router as permission
from app.routers.reviews_ratings import router as reviews_ratings
from app.models.category import Category
from app.models.products import Product
from sqlalchemy.schema import CreateTable

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def welcome() -> dict:
    return {"message": "My e-commerce app"}

app.include_router(category)
app.include_router(products)
app.include_router(auth)
app.include_router(permission)
app.include_router(reviews_ratings)
