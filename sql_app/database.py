from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import *

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Base.metadata.create_all(bind=engine)


def db_openish(func):
    def open_and_finish(*args, **kwargs):
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        res = func(db=db, *args, **kwargs)
        db.close()
        return res

    return open_and_finish
