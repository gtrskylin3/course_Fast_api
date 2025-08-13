"""
Gzip - это алгоритм сжатия.
Используется очень часто для сжатия контента,
передаваемого через Интернет, и учитывая,
что он поддерживается браузерами,
то он способен сильно уменьшить размер файлов JavaScript, CSS и HTML.
"""

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()

app.add_middleware(GZipMiddleware, minimum_size=1000)

# minimum_size- Не делать сжатие ответов, 
# которые меньше этого минимального размера в байтах. 
# По умолчанию 500.


@app.get("/")
async def main():
    return "somebigcontent"