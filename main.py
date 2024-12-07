from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from database import init_models


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield



app = FastAPI(lifespan=lifespan)


@app.get("/", summary="main endpoimt")
def hello():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)