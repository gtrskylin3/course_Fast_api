"""
Проверяет заголовок хоста 
входящих запросов для предотвращения 
потенциальных атак заголовка хоста HTTP.
"""

from fastapi import FastAPI
# cSpell:ignore trustedhost
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

app.add_middleware(
    TrustedHostMiddleware, 
    allow_hosts = ['example.com', '*.example.com']
)

@app.get("/")
async def main():
    return {"message": "Hello World"}