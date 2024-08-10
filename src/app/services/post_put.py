from os import remove
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Memes
from app.services.s3 import upload_file


async def post_memes(file: UploadFile, text: str, db: AsyncSession):
    if file.size < 1:
        raise HTTPException(status_code=422, detail=f"The file is too small")

    try:
        filename = f"{uuid4()}"
        path = await upload_file(filename=filename, file=file)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload error: {e}")

    try:
        item = Memes(text=text, path=path)
        db.add(item)
        await db.commit()

        return {
            "id": item.id,
            "text": item.text,
            "path": item.path,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


async def update_memes(upd_id: int, file: UploadFile, text: str, db: AsyncSession):
    try:
        query = select(Memes).where(Memes.id == upd_id)
        result = await db.execute(query)
        item = result.scalars().first()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No item with id {upd_id}: {e}")

    try:
        if file:
            try:
                filename = item.path.split("/")[-1]
                item.path = await upload_file(filename=filename, file=file)

            except Exception as e:
                raise HTTPException(status_code=500, detail=f"File upload error: {e}")

        if text:
            item.text = text

        await db.commit()

        response = {
            "id": item.id,
            "text": item.text,
            "path": item.path,
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
