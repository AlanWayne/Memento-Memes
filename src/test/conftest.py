from os import environ
from typing import AsyncGenerator

import pytest
from dotenv import load_dotenv
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.database.config import get_db
from main import app

load_dotenv()

DB_DRIV_TEST = environ.get("DB_DRIV_TEST")
DB_HOST_TEST = environ.get("DB_HOST_TEST")
DB_PORT_TEST = environ.get("DB_PORT_TEST")
DB_NAME_TEST = environ.get("DB_NAME_TEST")
DB_USER_TEST = environ.get("DB_USER_TEST")
DB_PASS_TEST = environ.get("DB_PASS_TEST")

url = f"{DB_DRIV_TEST}+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"
Base = declarative_base()
engine = create_async_engine(url, echo=True, poolclass=NullPool)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        yield db


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True, scope='session')
async def setup_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        yield async_client

# async def override_get_db() -> AsyncSession:
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


# @pytest.fixture(scope='session')
# async def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()
