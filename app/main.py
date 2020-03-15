from typing import List
from typing import Optional

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.testclient import TestClient
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from pydantic import BaseModel
import json


from . import submit_job
# from . import database

import argparse
import logging

from sqlalchemy.orm import Session
from .database import crud, models, schemas
from .database.database import SessionLocal, engine
from .utils import sql_queries
from . import constants


from enum import Enum, IntEnum


class QueueEnum(str, Enum):
    testtask_low = 'testtask-low'
    testtask_high = 'testtask-high'
    testtask_urgent = 'testtask-urgent'


class JobTypeEnum(str, Enum):
    testtask = 'testtask'


class JobRequest(BaseModel):
    queuename: QueueEnum = QueueEnum.testtask_low
    jobtype: JobTypeEnum
    jobargs: dict


class JobResponse(BaseModel):
    rqjobid: str
    # status: str

logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/jobs/", response_model=JobResponse)  #JSON
async def submit(request: JobRequest):
    logger.info(request)
    args =  request.dict()

    # args = eval(request.decode("utf-8"))
    logger.info(f'received args: {args}')

    job_details = await submit_job.submit_with_args(args)
    import pprint
    logger.info(f"submitted job: {pprint.pformat(job_details.__dict__)}")


    #-- returns the rq job id
    #-- this can be used to look up job status
    #-- using /jobs/<rqjobid>
    #-- this response structure has to conform response_model=JobResponse
    resp = {"rqjobid": job_details.id,
            #"status": job_details._status
            }

    #-- Instead if want to return any json, then remove the response_model,
    #-- and instead add `response_class=Response` in the @app.post definition
    #-- and return json.dumps(some_dict)

    return resp


# @app.get("/jobs/", response_model=List[schemas.Job])
# async def submit():
#     request = sql_queries.get_all_records()
#     logger.info(request)
#     return request


@app.get('/jobs/{rqjobid}', response_model=schemas.Job)
async def read_job(rqjobid: str, db: Session = Depends(get_db)):
    db_job = crud.get_job(db, rqjobid=rqjobid)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job


@app.get("/jobs/", response_model=List[schemas.Job])
def read_jobs(db: Session = Depends(get_db),
              skip: Optional[int] = 0,
              limit: Optional[int] = 100,
              status: Optional[str] = None):
    if status is not None and status not in constants.STATUS_CODES:
        raise HTTPException(
            status_code=404,
            detail={"error": f"Provide one of the supported status codes for filtering: {constants.STATUS_CODES}"})
    job = crud.get_jobs(db, skip=skip, limit=limit, status=status)
    return job


@app.delete("/jobs/", response_model=List[schemas.Job])
def delete_jobs(db: Session = Depends(get_db)):
    job = crud.delete_jobs(db)
    return job


@app.get("/", response_class=HTMLResponse)
def read_root():
    #return r"#Submit Jobs to Task Queues"
    html_content = """
    <html>
        <head>
            <title>Job Queuing Server</title>
        </head>
        <body>
            <h1>Submit jobs via POST request to  /jobs/</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)



if __name__ == '__main__':
    app.run()
