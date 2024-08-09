from os import environ
from pathlib import Path
from shutil import rmtree
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

load_dotenv()

DB_DRIV = environ.get("DB_DRIV")
DB_HOST = environ.get("DB_HOST")
DB_PORT = environ.get("DB_PORT")
DB_NAME = environ.get("DB_NAME")
DB_USER = environ.get("DB_USER")
DB_PASS = environ.get("DB_PASS")

url = f"{DB_DRIV}+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

Base = declarative_base()
engine = create_async_engine(url, echo=True, poolclass=NullPool)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        try:
            yield db
        except Exception as e:
            await db.rollback()
            raise e
        finally:
            await db.close()


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_model():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        rmtree("app/media/")
        Path("app/media").mkdir(parents=True, exist_ok=True)

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
