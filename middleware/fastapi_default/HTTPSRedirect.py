"""
Обеспечивает, чтобы все входящие запросы 
были либо  https Вместо этого любые входящие 
запросы к  http  будут перенаправлены на https.
"""

from fastapi import FastAPI
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware


app = FastAPI()

app.add_middleware(HTTPSRedirectMiddleware)


@app.get("/")
async def main():
    return {"message": "Hello World"}