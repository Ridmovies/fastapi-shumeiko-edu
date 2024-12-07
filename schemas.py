from pydantic import BaseModel, Field, ConfigDict


class BookAddSchema(BaseModel):
    title: str = Field(min_length=1, max_length=32)
    author: str

    model_config = ConfigDict(extra="forbid")

class BookSchema(BookAddSchema):
    id: int = Field(ge=0)