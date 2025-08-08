from fastapi import FastAPI, Request, status, Body, HTTPException, Form
from uvicorn import run
from schemas import Message
from typing import List
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates =  Jinja2Templates(directory="templates")

messages_db = []

@app.get("/")
async def get_all_messages(request: Request) -> HTMLResponse:
    # return messages_db
    return templates.TemplateResponse("message.html",
            {"request": request, "messages": messages_db})


@app.get("/message/{message_id}")
async def get_message(request: Request, message_id: int) -> HTMLResponse:
    # try:
    #     return messages_db[message_id]
    # except IndexError:
    #     raise HTTPException(status_code=404, 
    #                         detail="Message not found")
    try:
        return templates.TemplateResponse("message.html",
    {"request": request, "message": messages_db[message_id]})
    except IndexError:
        raise HTTPException(status_code=404, 
                            detail="Message not found")


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_message(
    request: Request, 
    message: str = Form()
) -> HTMLResponse:
    if len(messages_db) == 0:
        max_id_message = 0
    else:
        max_id_message = max([i.dict()['id'] for i in messages_db]) + 1
    messages_db.append(Message(id=max_id_message, text=message))
    return templates.TemplateResponse("message.html",
        {"request": request, "messages": messages_db})

@app.put("/message/{message_id}")
async def update_message(message_id: str, 
                         message: str = Body()) -> str:
    try:
        edit_message = messages_db[message_id]
        edit_message.text = message
        return f"Message updated!"
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.delete("/message/{message_id}")
async def delete_message(message_id: int) -> str:
    try:
        messages_db.pop(message_id)
        return f"Message ID={message_id} deleted!"
    except:
         raise HTTPException(status_code=404, detail="Message not found")

@app.delete("/")
async def kill_message_all() -> str:
    messages_db.clear()
    return "All messages deleted!"

if __name__ == "__main__":
    run("main:app", reload=True)