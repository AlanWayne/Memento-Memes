from app.database.models import Memes
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from fastapi import HTTPException
from uuid import uuid4
from os import remove
import requests
from pathlib import Path


async def delete_all(db: AsyncSession):
    try:
        query = select(Memes)
        result = await db.execute(query)
        items = result.scalars().all()

        for item in items:
            try:
                remove(item.path)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"No item found: {e}")

        query = delete(Memes)
        await db.execute(query)
        await db.commit()

        return f"Deleted: {len(items)} items"

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


async def fill_with_data(amount: int, db: AsyncSession):
    url = "https://loremflickr.com/640/360"

    responses = []

    for _ in range(amount):
        try:
            Path("app/media").mkdir(parents=True, exist_ok=True)
            uuid = uuid4()
            path = f"app/media/{uuid}.jpg"

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Path resolution error: {e}")

        try:
            with open(path, "wb") as write_file:
                response = requests.get(url=url)
                write_file.write(response.content)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File writing error: {e}")

        try:
            item = Memes(text=str(uuid).split("-")[1], path=path)
            db.add(item)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")

        response = {
            "id": item.id,
            "text": item.text,
            "path": item.path,
        }

        responses.append(response)

    await db.commit()

    return f"Items created: {responses}"
