from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.database.config import init_models, drop_model
from app.routers import memes, util


@asynccontextmanager
async def lifespan(lifespan_app: FastAPI):
    await init_models()
    yield
    await drop_model()


app = FastAPI(title="Memento Memes", lifespan=lifespan)
app.include_router(memes.router, prefix="")
app.include_router(util.router, prefix="")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
