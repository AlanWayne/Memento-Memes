from app.database.models import Memes
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
import asyncio


async def get_memes_all(page: int, limit: int, db: AsyncSession):
    page = page - 1 if page >= 0 else 1
    limit = limit if limit > 0 else 50

    try:
        query = select(Memes).offset(offset=page * limit).limit(limit=limit)
        result = await db.execute(query)
        response = (
            result.scalars().all()
        )

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_memes_by_id(get_id: int, db: AsyncSession):
    try:
        # response = db.query(Memes).filter(Memes.id == get_id).first()
        query = select(Memes).where(Memes.id == get_id)
        result = await db.execute(query)
        response = result.scalars().first()
        if response is None:
            return HTTPException(status_code=500, detail="No record with such id")
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
