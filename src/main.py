import uvicorn
from fastapi import FastAPI
from app.database.config import engine, Base
from app.routers import memes, util

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(memes.router, prefix="")
app.include_router(util.router, prefix="")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
