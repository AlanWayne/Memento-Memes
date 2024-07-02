import uvicorn
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import router

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(router, prefix="")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
