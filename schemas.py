from pydantic import BaseModel, Field, ConfigDict


class BookSchema(BaseModel):
    title: str = Field(min_length=1, max_length=32)
    author: str
    age: int = Field(ge=0, le=100)

    model_config = ConfigDict(extra="forbid")