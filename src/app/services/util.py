from os import remove
from uuid import uuid4

import requests
from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Memes
from app.services.s3 import delete_file, upload_raw


async def delete_all(db: AsyncSession):
    try:
        query = select(Memes)
        result = await db.execute(query)
        items = result.scalars().all()

        for item in items:
            try:
                filename = item.path.split("/")[-1]
                item.path = await delete_file(filename=filename)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"No item found: {e}")

        query = delete(Memes)
        await db.execute(query)
        await db.commit()

        return f"Deleted: {len(items)} items"

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


async def fill_with_data(amount: int, db: AsyncSession):
    url_img = "https://loremflickr.com/640/360"
    url_txt = "https://api.api-ninjas.com/v1/loremipsum?max_length=10&random=true"

    responses = []

    for _ in range(amount):
        try:
            with open("app/temp", "wb") as file:
                response = requests.get(url=url_img)
                file.write(response.content)

            with open("app/temp", "rb") as file:
                filename = f"{uuid4()}"
                path = await upload_raw(filename=filename, file=file)

            remove("app/temp")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File upload error: {e}")

        try:
            response = requests.get(url=url_txt, headers={'X-Api-Key': 'QsbmNxqn9sx2tKoBXg9maw==H7sVlgW20fSJEYzy'})
            item = Memes(text=str(response.text), path=path)
            db.add(item)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")

        response = {
            "id": item.id,
            "text": item.text,
            "path": item.path,
        }

        responses.append(response)

    try:
        await db.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    return f"Items created: {responses}"
