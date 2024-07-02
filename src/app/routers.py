from fastapi import APIRouter, Depends, UploadFile, File, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import *

router = APIRouter()


@router.get("/memes/", tags=["GET"])
async def get_memes_all_url(db: Session = Depends(get_db)):

    return get_memes_all(db=db)


@router.get("/memes/{id}", tags=["GET"])
async def get_memed_by_id_url(id: int = None, db: Session = Depends(get_db)):

    return get_memes_by_id(id=id, db=db)


@router.post("/memes/", tags=["POST/PUT"])
async def post_memes_url(
    file: UploadFile = File(...), text: str = Body(...), db: Session = Depends(get_db)
):

    return post_memes(file=file, text=text, db=db)


@router.put("/memes/{id}", tags=["POST/PUT"])
async def update_memes_url(
    id: int = None,
    file: UploadFile = File(None),
    text: str = Body(None),
    db: Session = Depends(get_db),
):

    return update_memes(id=id, file=file, text=text, db=db)


@router.delete("/memes/", tags=["DELETE"])
async def delete_all_url(db: Session = Depends(get_db)):

    return delete_all(db)


@router.delete("/memes/{id}", tags=["DELETE"])
async def delete_by_id_url(id: int, db: Session = Depends(get_db)):

    return delete_by_id(id, db)
