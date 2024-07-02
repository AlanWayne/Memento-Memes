from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.config import get_db
from app.services import util
import asyncio

router = APIRouter()


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
