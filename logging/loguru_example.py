from fastapi import FastAPI
from loguru import logger

app =  FastAPI()

logger.add("info.log")

@app.get("/{name}")
async def hello_page(name):
    logger.info("Hello from root page")
    hello_world()
    return {"message": f"Hello {name}"}

def hello_world():
    logger.info("hello() called")

    