from app.database.models import Memes
from sqlalchemy.orm import Session
from fastapi import HTTPException
from os import remove


def delete_by_id(id: int, db: Session):

    try:
        item = db.query(Memes).filter(Memes.id == id).first()

        try:
            remove(item.path)
        except:
            pass

        response = {
            "id": item.id,
            "text": item.text,
            "path": item.path,
        }

        db.delete(item)
        db.commit()

        return f"Deleted: {response}"

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
