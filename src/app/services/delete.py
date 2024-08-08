from os import remove

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Memes


async def delete_by_id(del_id: int, db: AsyncSession):
    try:
        result = await db.execute(select(Memes).where(Memes.id == del_id))
        item = result.scalars().first()

        try:
            remove(item.path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        response = {
            "id": item.id,
            "text": item.text,
            "path": item.path,
        }

        await db.delete(item)
        await db.commit()

        return f"Deleted: {response}"

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
