import time
from fastapi import FastAPI

app = FastAPI()

def call_background_task(message):
    time.sleep(10)
    print(f"Background Task called!")
    print(message)


# @app.get('/')
# async def hello_world():
#     call_background_task()
#     return {"message": "Hello, World!"}

"блокирует выполнение всей проги на 10 сек"
# Запрос блокируется, т.е. требуется 10 секунд.

# Если мы отправим более 1 запроса, они не будут обрабатываться 
# параллельно. Мы можем это проверить открыв несколько вкладок.
# Чтобы улучшить работу, мы можем убрать логику выполнения
#  в фоновом режиме. Для этого мы 
# можем использовать класс BackgroundTasks.

from fastapi import BackgroundTasks

@app.get("/")
async def hello_world(message: str, background_task: BackgroundTasks):
    background_task.add_task(call_background_task, message) 
    #Если фоновому процессу требуются аргументы, 
    # мы передаем эти аргументы в функцию add_task()
    #  сразу после ее первого параметра. 
    return {'message': 'Hello World!'}


# На данный момент у него нет некоторых расширенных функций,
# таких как повторение задачи, оркестровка задач,
# отслеживание задачи или ее отмена.
# Другое основное ограничение заключается в том,
# что когда мы выполняем сверхтяжелые вычисления,
# мы можем не хотеть, чтобы задача выполнялась в том же процессе.
# Иногда мы можем захотеть распределить задачи по нескольким серверам.
# В таких случаях Celery является одной из лучших альтернатив.