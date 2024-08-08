from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base
import os
from typing import AsyncGenerator
import asyncio

load_dotenv()

DB_DRIV = os.environ.get("DB_DRIV")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

url = f"{DB_DRIV}+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

Base = declarative_base()
engine = create_async_engine(url, echo=True, poolclass=NullPool)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        yield db


# async def get_db() -> AsyncSession:
#     async with engine.begin() as connection:
#         await connection.run_sync(Base.metadata.create_all)
#     db = SessionLocal()
#     try:
#         yield db
#     except Exception as e:
#         await db.rollback()
#         raise e
#     finally:
#         await db.close()
