import logging
import time

from . import database
from .database import crud, models, schemas
from .database.database import SessionLocal, engine


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


def _show():
    import sqlite3

    # Create a SQL connection to our SQLite database
    con = sqlite3.connect("data/jobstatus.db")

    cur = con.cursor()

    # The result of a "cursor.execute" can be iterated over by row
    for row in cur.execute('SELECT * FROM jobs;'):
        print(row)

    # Be sure to close the connection
    con.close()


if __name__ == '__main__':
    db = get_db()
    job = schemas.Job(jobid='abcde',
                      queuename='test-queue',
                      jobtype='testjobtype',
                      rqid=f'testrqid+{time.time()}')
    try:
        crud.create_job(db, job)
    except:
        pass

    db = get_db()

    job = schemas.Job(jobid=time.time(),
                      queuename='test-queue',
                      jobtype='testjobtype',
                      rqid=f'testrqid+{time.time()}')
    logger.info(f'Job: {job}')
    crud.create_job(db, job)


    _show()

    logger.info('Updating record')
    import datetime as dt
    from .database.models import Job

    # db = get_db()
    # job = schemas.Job(finishedat=dt.datetime.now(),
    #                   jobtype='testjobtype2')
    # db.query(Job).filter(Job.jobid == 'abcde').update(**{k:v for k,v in job.dict().items() if v is not None})

    db.query(Job).filter(Job.jobid == 'abcde').update(
        {Job.finishedat: dt.datetime.now()})
    db.commit()

    # update_statement = (db.query(models.Job).update()
    #                     .where(Job.jobid == 'abcde')
    #                     .values(finishedat = dt.datetime.now())
    #                     )
    # db.execute(update_statement)

    # query = db.query(models.Job).filter(models.Job.jobid == 'abcde')
    # db.execute(query)
    # logger.info(query)
    # query = db.query(models.Job).filter(models.Job.jobid == 'abcde')
    # query.update({models.Job.finishedat:dt.datetime.now()})
    # db.execute(query.update({models.Job.finishedat: dt.datetime.now()}))
    # db.commit()

    # logger.info(schemas.Job
    # print(schemas.Job.update)

    # stored_data = db.query(models.Job).filter(models.Job.jobid == 'abcde').first()
    # logger.info(stored_data)
    # logging.info(stored_data.__dict__)
    # stored_model = schemas.Job(**stored_data.__dict__)
    # logger.info(f'stored_model: {stored_model}')
    _show()





    # for row in db.query(Job).all():
    #     print(row)
