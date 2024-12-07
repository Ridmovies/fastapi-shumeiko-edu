from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    pass
    yield



app = FastAPI(lifespan=lifespan)


@app.get("/")
def hello():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)