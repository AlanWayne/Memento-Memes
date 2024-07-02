from sqlalchemy import Column, Integer, String, ForeignKey, Text
from app.database import Base


class Memes(Base):
    __tablename__ = "memes"

    id = Column(Integer, primary_key=True)
    text = Column(Text, default="")
    path = Column(String, unique=True, default="")
