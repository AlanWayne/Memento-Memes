from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import *

router = APIRouter()

# document

@router.post("/upload/", tags=["document"])
async def upload(data: UploadFile = None, db: Session = Depends(get_db)):
    return upload_doc(data, db)


@router.put("/analys/", tags=["document"])
async def analys(id: int = None, db: Session = Depends(get_db)):
    return analyse_doc(id, db)


@router.get("/extract/", tags=["document"])
async def extract(id: int = None, db: Session = Depends(get_db)):
    return get_text(id, db)


@router.delete("/delete/", tags=["document"])
async def delete(id: int = None, db: Session = Depends(get_db)):
    return remove_doc(id, db)

# log

@router.get("/healthcheck/", tags=["log"])
async def health_check():
    return {"status": True}
