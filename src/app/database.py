from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

url = URL.create(
    drivername="postgresql",
    username=f"{DB_USER}",
    host=f"{DB_HOST}",
    database=f"{DB_NAME}",
    password=f"{DB_PASS}",
    # port=f"{DB_PORT}",
)

engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
