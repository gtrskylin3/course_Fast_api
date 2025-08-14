import time

from fastapi import FastAPI, BackgroundTasks

app = FastAPI()


def call_background_task(message):
    time.sleep(10)
    print(f"Background Task called!")
    print(message)


@app.get("/")
async def hello_world(message: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(call_background_task, message)
    return {'message': 'Hello World!'}

# Celery — это неблокирующая очередь задач,
#  работающая в распределенной системе.
#  Он может управлять асинхронными фоновыми процессами,
#  которые огромны и требуют большой нагрузки на процессор.
#  Это сторонний инструмент, поэтому сначала нам нужно установить его:

# pip install Celery

# Он планирует и выполняет задачи одновременно 
# на одном сервере или в распределенной среде. 
# Но для отправки и получения сообщений требуется транспорт сообщений,
# такой как Redis, база данных в памяти, 
# которую можно использовать в качестве брокера сообщений
# для сообщений в строках, словарях, списках, наборах, 
# растровых изображениях и типах потоков.

