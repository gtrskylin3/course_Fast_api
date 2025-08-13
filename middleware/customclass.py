# CustomMiddleware на основе классов

from fastapi import FastAPI
import time




class TimingMiddleware:
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        start_time = time.time()
        await self.app(scope, receive, send)
        duration = time.time() - start_time
        print(f"Request duration: {duration:.5f} sec")

"""
Важной частью этого класса является метод __call__, 
который реализует спецификацию приложения ASGI. 
Это асинхронная функция, которая принимает scope, receive и send. 
Эти параметры необходимы для запроса FastAPI.
 В этом простом Middleware мы просто передаем их в наше приложение FastAPI 
 в  self.app. 
"""

app = FastAPI()
app.add_middleware(TimingMiddleware)


@app.get("/hello")
async def greeter():
    return {"Hello": "World"}


@app.get("/goodbye")
async def farewell():
    return {"Goodbye": "World"}


