"""
SessionMiddleware
Сессия сайта — это механизм, который позволяет 
сайту помнить о пользователях и сохранять сделанные ими действия.
Сессии используются для разных целей, например:
для сохранения введённых пользователем данных; 
для настройки выдачи под интересы пользователя; 
для показа персональных предложений в зависимости от действий на сайте.
"""
import uvicorn
from shop_fastapi.app.config import settings


from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware,
    secret_key=settings.SECRET_KEY
)

# pip install itsdangerous

# Чтобы добавить данные сеанса в наш код, 
# нам нужно внедрить Request в каждую службу конечной точки 
# и использовать ее словарь сеанса для хранения объектов области сеанса.

@app.get('/create_session')
async def session_set(request: Request):
    request.session['my_session'] = '1234'
    return 'ok'

@app.get('/read_session')
async def session_info(request: Request):
    my_var = request.session.get("my_session")
    return my_var


@app.delete('/delete_session')
async def delete_session(request: Request):
    my_var =request.session.pop("my_session")
    return my_var


if __name__ == "__main__":
    uvicorn.run("middleware.session:app", reload=True)

