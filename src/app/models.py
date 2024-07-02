from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class Document(Base):
    __tablename__ = "document"

    id = Column(Integer, primary_key=True)
    path = Column(String)


class Documents_text(Base):
    __tablename__ = "documents_text"

    id = Column(Integer, primary_key=True)
    id_doc = Column(Integer, ForeignKey("document.id"), unique=True)
    text = Column(String)
