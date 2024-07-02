from app.models import Memes
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile, Depends
from uuid import uuid4
from os import remove, system
from app.database import SessionLocal


def get_memes_all(db: Session):

    try:
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


def post_memes(file: UploadFile, text: str, db: Session):

    if file.size < 1:
        raise HTTPException(status_code=422, detail=f"The file is too small")

    try:
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

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    return {
        "id": item.id,
        "text": item.text,
        "path": item.path,
    }


def update_memes(id: int, file: UploadFile, text: str, db: Session):

    try:
        item = db.query(Memes).filter(Memes.id == id).first()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No item with id {id}: {e}")

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


system('psql db_memes -c "select * from memes;"')
