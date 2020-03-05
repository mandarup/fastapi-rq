import datetime as dt

from pydantic import BaseModel

from .. import constants


class Job(BaseModel):
    id: int = None
    jobid : str = None
    rqjobid: str
    jobtype: str
    queuename: str
    status: str = constants.STATUS_QUEUED
    args: str = None
    createdat: dt.datetime = dt.datetime.now()
    startedat: dt.datetime = None
    finishedat: dt.datetime = None
    jobinfo:str = None
    error:str = None
    result: str = None
    # waittime: dt.timedelta = None
    # runtime: dt.datetime = None

    class Config:
        orm_mode = True