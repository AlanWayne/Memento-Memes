from fastapi import APIRouter, Depends, UploadFile, File, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.config import get_db
from app.services import get, post_put, delete

router = APIRouter()


@router.get("/memes/", tags=["GET"])
async def get_memes_all_url(
        page: int = 1, limit: int = 50, db: AsyncSession = Depends(get_db)
):
    return await get.get_memes_all(page=page, limit=limit, db=db)

#
# @router.get("/memes/{id}", tags=["GET"])
# async def get_memed_by_id_url(get_id: int = None, db: AsyncSession = Depends(get_db)):
#     return get.get_memes_by_id(get_id=get_id, db=db)
#
#
# @router.post("/memes/", tags=["POST/PUT"])
# async def post_memes_url(
#         file: UploadFile = File(...), text: str = Body(...), db: AsyncSession = Depends(get_db)
# ):
#     return post_put.post_memes(file=file, text=text, db=db)
#
#
# @router.put("/memes/{id}", tags=["POST/PUT"])
# async def update_memes_url(
#         upd_id: int = None,
#         file: UploadFile = File(None),
#         text: str = Body(None),
#         db: AsyncSession = Depends(get_db),
# ):
#     return post_put.update_memes(upd_id=upd_id, file=file, text=text, db=db)
#
#
# @router.delete("/memes/{id}", tags=["DELETE"])
# async def delete_by_id_url(del_id: int, db: AsyncSession = Depends(get_db)):
#     return delete.delete_by_id(del_id=del_id, db=db)

