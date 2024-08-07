from sqlalchemy import Column, Integer, String, Text
from app.database.config import Base
from pydantic import BaseModel


class Memes(Base):
    __tablename__ = "memes"

    id = Column(Integer, primary_key=True)
    text = Column(Text, default="")
    path = Column(String, unique=True, default="")


class MemesBase(BaseModel):
    id: int
    text: str
    path: str
