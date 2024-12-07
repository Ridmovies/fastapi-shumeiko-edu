from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from database import init_models
from schemas import BookSchema


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield


books = [{
    "title": "The Hobbit", "author": "J.R.R. Tolkien", "age": 30
}]


app = FastAPI(lifespan=lifespan)

@app.get("/books")
def get_book_list() -> list[BookSchema]:
    return books


@app.get("/books/{book_id}")
def get_book(book_id: int) -> BookSchema:
    book = books[book_id]
    return book


@app.post("/books", summary="add book", tags=["books"])
def add_book(book: BookSchema):
    books.append(book)
    return {"message": "Book added"}

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)