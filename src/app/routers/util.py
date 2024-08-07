from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.config import get_db
from app.services import util
import asyncio

router = APIRouter()


@router.delete("/util/", tags=["UTIL"])
async def delete_all_url(db: AsyncSession = Depends(get_db)):
    return await util.delete_all(db=db)


@router.post("/util/", tags=["UTIL"])
async def fill_with_data_url(amount: int = 1, db: AsyncSession = Depends(get_db)):
    return await util.fill_with_data(amount=amount, db=db)

