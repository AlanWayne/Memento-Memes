from app.models import Document, Documents_text
from sqlalchemy.orm import Session
from fastapi import UploadFile
from os import remove
from celery import Celery
from PIL import Image
from pytesseract import pytesseract
from app.config import REDIS_HOST, REDIS_PORT

celery = Celery(
    "tasks",
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}",
)


def upload_doc(file: UploadFile, db: Session):
    try:
        temp_path = f"/app/Documents/{file.filename}"
        document = Document(path=temp_path)
    except Exception as exception:
        print(exception)
        return 1
    else:

        try:
            with open(temp_path, "wb") as f:
                f.write(file.file.read())
        except Exception as exception:
            print(exception)
            return 1
        else:
            db.add(document)
            db.commit()
            db.refresh(document)
            return temp_path


def remove_doc(id: int, db: Session):
    try:
        db.query(Documents_text).filter(Documents_text.id_doc == id).delete()
    except Exception as exception:
        print(exception)

    try:
        document = db.query(Document).filter(Document.id == id).first()
    except Exception as exception:
        print(exception)
    else:
        try:
            remove(document.path)
        except Exception as exception:
            print(exception)

        try:
            db.query(Document).filter(Document.id == id).delete()
        except Exception as exception:
            print(exception)

    db.commit()

    return 0


def analyse_doc(id: int, db: Session):
    try:
        image_path = db.query(Document).filter(Document.id == id).first().path
    except Exception as exception:
        print(exception)
        return 1
    else:
        try:
            text_result = image_to_text.delay(image_path).get()
            if text_result == 1:
                raise FileNotFoundError
        except Exception as exception:
            print(exception)
            return 2
        else:
            document_text = Documents_text(id_doc=id, text=text_result)
            db.add(document_text)
            db.commit()
            db.refresh(document_text)
            return document_text


@celery.task
def image_to_text(path):
    try:
        image = Image.open(path)
        pytesseract.tesseract_cmd = r"/usr/bin/tesseract"
        text = pytesseract.image_to_string(image)
    except Exception as exception:
        print(exception)
        return 1
    else:
        return text


def get_text(id: int, db: Session):
    try:
        text = db.query(Documents_text).filter(Documents_text.id_doc == id).first().text
    except Exception as exception:
        print(exception)
        return 1
    else:
        return text
