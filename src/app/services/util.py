from app.database.models import Memes
from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import uuid4
from os import remove
import requests


def delete_all(db: Session):

    try:
        items = db.query(Memes).all()

        for item in items:
            try:
                remove(item.path)
            except:
                pass

        response = db.query(Memes).delete()
        db.commit()

        return f"Deleted: {response} record(s)"

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


async def fill_with_data(amount: int, db: Session):
    url = "https://loremflickr.com/640/360"

    response = requests.get(url=url)
    uuid = uuid4()

    try:
        path = f"app/media/{uuid}.jpg"

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Path resolution error: {e}")

    try:
        with open(path, "wb") as write_file:
            write_file.write(response.content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File writing error: {e}")

    try:
        item = Memes(text=str(uuid).split("-")[1], path=path)
        db.add(item)
        db.commit()

        response = {
            "id": item.id,
            "text": item.text,
            "path": item.path,
        }

        return f"Items created: {response}"

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
