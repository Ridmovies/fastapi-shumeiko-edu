from pydantic import BaseModel

from database import Base


class Book(BaseModel):
    __tablename__ = 'books'
    title: str
    author: str