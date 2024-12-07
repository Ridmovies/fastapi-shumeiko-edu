from contextlib import asynccontextmanager

from authx import AuthXConfig, AuthX, RequestToken
from fastapi import FastAPI, Depends, HTTPException, Response
import uvicorn
from pydantic import BaseModel
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from database import init_models, get_db, session_depends
from models import Book
from schemas import BookSchema, BookAddSchema
from auth.views import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield


app = FastAPI(lifespan=lifespan)
# app.include_router(auth_router, prefix="/auth", tags=["auth"])


config = AuthXConfig(
     JWT_ALGORITHM = "HS256",
     JWT_SECRET_KEY = "SECRET_KEY",
     JWT_ACCESS_COOKIE_NAME = "access_token",
     JWT_TOKEN_LOCATION = ["cookies"],
)

auth = AuthX(config=config)
auth.handle_errors(app)

class UserLoginSchema(BaseModel):
    login: str
    password: str

@app.get('/login', tags=["auth"])
def login(username: str, password: str, response: Response):
     if username == "xyz" and password == "xyz":
          token = auth.create_access_token(uid=username)
          response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, value=token)
          return {"access_token": token}
     raise HTTPException(401, detail={"message": "Invalid credentials"})


@app.get("/protected", dependencies=[Depends(auth.access_token_required)], tags=["auth"])
def get_protected():
     return {"access_token": "ok"}


@app.get("/books")
async def get_book_list(session: session_depends) -> list[BookSchema]:
    stmt = select(Book).order_by(Book.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


@app.get("/books/{book_id}")
async def get_book(book_id: int, session: session_depends) -> BookSchema:
    book = await session.get(Book, book_id)
    return book


@app.post("/books", summary="add book", tags=["books"])
async def add_book(data: BookAddSchema, session: session_depends):
    new_book: Book = Book(title=data.title, author=data.author)
    session.add(new_book)
    await session.commit()
    return {"message": "Book added"}

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)