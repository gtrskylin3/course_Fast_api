from pydantic import BaseModel, Field

# class Message(BaseModel):
#     id: int
#     description: str | None = Field(default=None,
#                                     description="The description of the message",
#                                     max_length=300)
#     text: str = "Simple text"

class Message(BaseModel):
    id: int = None
    text: str 

    model_config = {
        "json_schema_extra": {
            "examples":
                [
                    {
                        "text": "Simple message",
                    }
                ]
        }
    }