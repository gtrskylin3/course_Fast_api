from fastapi import FastAPI, Depends, Query, HTTPException, status
from uvicorn import run
from pydantic import BaseModel

class Post(BaseModel):
    id: int
    text: str

db = []

app = FastAPI()

async def get_post_or_404(id: int):
    try:
        return db[id]
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.get("/message/{id}")
async def get_message(post: Post = 
                      Depends(get_post_or_404)):
    return post

@app.post("/message", status_code=status.HTTP_201_CREATED)
async def create_message(post: Post) -> str:
    post.id = len(db)
    db.append(post)
    return f"Message Created"


async def pagintation_func(limit: int = Query(10, ge=0), 
                           page: int = 1):
    return [{'limit': limit, 'page': page}]



@app.get("/messages")
async def all_messages(pagination: dict = Depends(pagintation_func)):
    return {"messages": pagination}


@app.get("/comments")
async def all_messages(pagination: dict = Depends(pagintation_func)):
    return {"messages": pagination}

if __name__ == "__main__":
    run("main:app", reload=True)