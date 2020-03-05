from typing import List

from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

# import os, sys
# sys.path.append(os.path.dirname(os.path.realpath(__file__)))


models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()