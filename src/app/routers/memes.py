from fastapi import APIRouter, Depends, UploadFile, File, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.config import get_db
from app.services import get, post_put, delete

router = APIRouter()


@router.get("/memes/", tags=["GET"])
async def get_memes_all_url(
        page: int = 1, limit: int = 50, db: AsyncSession = Depends(get_db)
):
    """
    Get information about all memes

    - **page**: go to the page number <page>
    - **limit**: amount of memes on page
    """
    return await get.get_memes_all(page=page, limit=limit, db=db)


#
@router.get("/memes/{get_id}", tags=["GET"])
async def get_memed_by_id_url(get_id: int = None, db: AsyncSession = Depends(get_db)):
    """
    Get information about spesific meme

    - **id**: specify id of the desired meme
    """
    return await get.get_memes_by_id(get_id=get_id, db=db)


@router.post("/memes/", tags=["POST/PUT"])
async def post_memes_url(
        file: UploadFile = File(...), text: str = Body(...), db: AsyncSession = Depends(get_db)
):
    """
    Add new meme to the base

    - **file**: upload your image
    - **text**: meme description
    """
    return await post_put.post_memes(file=file, text=text, db=db)


@router.put("/memes/{upd_id}", tags=["POST/PUT"])
async def update_memes_url(
        upd_id: int = None,
        file: UploadFile = File(None),
        text: str = Body(None),
        db: AsyncSession = Depends(get_db),
):
    """
    Change specific meme in the base

    - **id**: specify id of the desired meme
    - **file**: upload new image
    - **text**: set new meme description
    """
    return await post_put.update_memes(upd_id=upd_id, file=file, text=text, db=db)


@router.delete("/memes/{del_id}", tags=["DELETE"])
async def delete_by_id_url(del_id: int, db: AsyncSession = Depends(get_db)):
    """
    Remove specific meme from the base

    - **id**: specify id of the meme to remove
    """
    return await delete.delete_by_id(del_id=del_id, db=db)
