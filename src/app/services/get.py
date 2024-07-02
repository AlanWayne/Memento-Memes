from app.database.models import Memes
from sqlalchemy.orm import Session
from fastapi import HTTPException


def get_memes_all(page: int, limit: int, db: Session):

    page -= 1

    try:
        if limit > 0 and page >= 0:
            response = (
                db.query(Memes).offset(offset=page * limit).limit(limit=limit).all()
            )
        else:
            response = db.query(Memes).all()

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_memes_by_id(id: int, db: Session):

    try:
        response = db.query(Memes).filter(Memes.id == id).first()

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
