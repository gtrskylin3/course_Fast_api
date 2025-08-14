from fastapi import FastAPI, Request
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


# logging
from loguru import logger

logger.add(
    "info.log",
    format="Log: [{extra[log_id]}:{time} - {level} - {message}]",
    level="INFO",
    enqueue=True,
)

# LOGGING MIDDLEWARE FUNC
from uuid import uuid4
# from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    log_id = str(uuid4())
    with logger.contextualize(log_id=log_id):
        try:
            response = await call_next(request)
            if response.status_code in [401, 402, 403, 404]:
                logger.warning(f"Request to {request.url.path} failed")
            else:
                logger.info("Successfully accessed" + request.url.path)
        except Exception as e:
            logger.error(f"Request to {request.url.path} failed: {e}")
            response = JSONResponse(content={'success': False}, status_code=500)
        return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend URL
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
