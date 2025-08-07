from fastapi import FastAPI, status, Body
from uvicorn import run
from schemas import Message
app = FastAPI()

messages_db = []


@app.get("/")
async def get_all_messages() -> dict:
    return {'Messages': messages_db}


@app.get("/message/{message_id}")
async def get_message(message_id: int):
     return messages_db[message_id]


@app.post("/message", status_code=status.HTTP_201_CREATED)
async def create_message(message: Message) -> str:
    if len(messages_db) == 0:
        message.id = 0
    else:
        message.id = max([i.dict()['id'] for i in messages_db]) + 1
    messages_db.append(message)
    return f"Message created!"

@app.put("/message/{message_id}")
async def update_message(message_id: str, 
                         message: str = Body()) -> str:
    messages_db[message_id] = message
    return f"Message updated!"


@app.delete("/message/{message_id}")
async def delete_message(message_id: str) -> str:
    messages_db.pop(message_id)
    return f"Message ID={message_id} deleted!"

@app.delete("/")
async def kill_message_all() -> str:
    messages_db.clear()
    return "All messages deleted!"

if __name__ == "__main__":
    run("main:app", reload=True)