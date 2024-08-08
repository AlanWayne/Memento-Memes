from os import remove
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Memes


async def post_memes(file: UploadFile, text: str, db: AsyncSession):
    if file.size < 1:
        raise HTTPException(status_code=422, detail=f"The file is too small")

    try:
        Path("app/media").mkdir(parents=True, exist_ok=True)
        path = f"app/media/{uuid4()}.{file.filename.split('.')[-1]}"

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Path resolution error: {e}")

    try:
        with open(path, "wb") as write_file:
            file.file.seek(0)
            write_file.write(file.file.read())

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File writing error: {e}")

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
                remove(item.path)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

            try:
                Path("app/media").mkdir(parents=True, exist_ok=True)
                path = f"app/media/{uuid4()}.{file.filename.split('.')[-1]}"
                item.path = path

            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Path resolution error: {e}")

            try:
                with open(path, "wb") as write_file:
                    file.file.seek(0)
                    write_file.write(file.file.read())

            except Exception as e:
                raise HTTPException(status_code=500, detail=f"File writing error: {e}")

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
