from fastapi import APIRouter, Depends, UploadFile, File, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import get, post_put, delete, util
import asyncio

router = APIRouter()


@router.get("/memes/", tags=["GET"])
async def get_memes_all_url(
    page: int = 1, limit: int = 50, db: Session = Depends(get_db)
):

    return get.get_memes_all(page=page, limit=limit, db=db)


@router.get("/memes/{id}", tags=["GET"])
async def get_memed_by_id_url(id: int = None, db: Session = Depends(get_db)):

    return get.get_memes_by_id(id=id, db=db)


@router.post("/memes/", tags=["POST/PUT"])
async def post_memes_url(
    file: UploadFile = File(...), text: str = Body(...), db: Session = Depends(get_db)
):

    return post_put.post_memes(file=file, text=text, db=db)


@router.put("/memes/{id}", tags=["POST/PUT"])
async def update_memes_url(
    id: int = None,
    file: UploadFile = File(None),
    text: str = Body(None),
    db: Session = Depends(get_db),
):

    return post_put.update_memes(id=id, file=file, text=text, db=db)


@router.delete("/memes/{id}", tags=["DELETE"])
async def delete_by_id_url(id: int, db: Session = Depends(get_db)):

    return delete.delete_by_id(id, db)


@router.delete("/util/", tags=["UTIL"])
async def delete_all_url(db: Session = Depends(get_db)):

    return util.delete_all(db)


@router.post("/util/", tags=["UTIL"])
async def fill_with_data_url(amount: int = 1, db: Session = Depends(get_db)):

    tasks = []

    for _ in range(amount):
        task = asyncio.create_task(util.fill_with_data(amount, db))
        tasks.append(task)

    response = await asyncio.gather(*tasks)

    return response


# await asyncio.to_thread(system, 'psql db_memes -c "select * from memes;"')
