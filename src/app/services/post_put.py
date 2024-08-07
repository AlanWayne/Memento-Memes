from app.database.models import Memes
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, UploadFile
from uuid import uuid4
from pathlib import Path


def post_memes(file: UploadFile, text: str, db: AsyncSession):
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
        db.commit()

        return {
            "id": item.id,
            "text": item.text,
            "path": item.path,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


def update_memes(upd_id: int, file: UploadFile, text: str, db: AsyncSession):
    try:
        item = db.query(Memes).filter(Memes.id == upd_id).first()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No item with id {upd_id}: {e}")

    try:
        if file:
            item.file = file

        if text:
            item.text = text

        db.commit()

        response = {
            "id": item.id,
            "text": item.text,
            "path": item.path,
        }

        return f"Updated: {response}"

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
