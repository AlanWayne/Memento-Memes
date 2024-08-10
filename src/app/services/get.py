from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Memes


async def get_memes_all(page: int, limit: int, db: AsyncSession):
    page = page - 1 if page >= 0 else 1
    limit = limit if limit > 0 else 50

    try:
        query = select(Memes).offset(offset=page * limit).limit(limit=limit)
        result = await db.execute(query)
        response = (
            result.scalars().all()
        )

        if response.__len__() == 0:
            return "No records in database"

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(f"No connection to database {e}"))


async def get_memes_by_id(get_id: int, db: AsyncSession):
    try:
        query = select(Memes).where(Memes.id == get_id)
        result = await db.execute(query)
        response = result.scalars().first()
        if response is None:
            return HTTPException(status_code=500, detail="No record with such id")
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
