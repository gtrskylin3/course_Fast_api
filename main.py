from fastapi import FastAPI, status, Body
from uvicorn import run
app = FastAPI()

messages_db = {"0": "First post in FastAPI"}


@app.get("/")
async def get_all_messages() -> dict:
    return messages_db


@app.get("/message/{message_id}")
async def get_message(message_id: str) -> str:
     return messages_db[message_id]


@app.post("/message", status_code=status.HTTP_201_CREATED)
async def create_message(message: str = Body()) -> str:
    current_index = len(messages_db)
    messages_db[current_index] = message
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