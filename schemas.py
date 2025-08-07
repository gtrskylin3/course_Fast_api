from pydantic import BaseModel, Field

# class Message(BaseModel):
#     id: int
#     description: str | None = Field(default=None,
#                                     description="The description of the message",
#                                     max_length=300)
#     text: str = "Simple text"

class Message(BaseModel):
    id: int
    text: str 

