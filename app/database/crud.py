import datetime
import dateutil
from sqlalchemy.orm import Session

from . import models, schemas


def get_job(db: Session, rqjobid: str):
    return db.query(models.Job).filter(models.Job.rqjobid == rqjobid).first()


def get_jobs(db: Session, skip: int = 0, limit: int = 100, status:str=None):
    if status is None:
        return db.query(models.Job).offset(skip).limit(limit).all()
    else:
        cond = models.Job.status == status
        return db.query(models.Job).filter(cond).offset(skip).limit(limit).all()


def delete_jobs(db: Session):
    relative_date = datetime.datetime.now() + dateutil.relativedelta.relativedelta(days=-7)
    cond = models.Job.finishedat <= relative_date
    db.query(models.Job).filter(cond).delete()

    # created more than N days and never finished, delete them
    relative_date = datetime.datetime.now() + dateutil.relativedelta.relativedelta(days=-7)
    cond1 = models.Job.createdat <= relative_date
    cond2 = models.Job.finishedat == None
    db.query(models.Job).filter(cond1).filter(cond2).delete()
    db.commit()

def create_job(db: Session, job: schemas.Job):
    db_job = models.Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


# def update_job(job:schemas.Job):
#     db = get_db()
#     db.query(Job).filter(Job.jobid == 'abcde').update(
#         {Job.finishedat: dt.datetime.now()})
#     db.commit()
