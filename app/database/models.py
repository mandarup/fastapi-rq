from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Interval
from sqlalchemy.orm import relationship
import datetime as dt

import sys
#-- Add higher directory to python modules path.
#-- This makes it possible to import from ..
sys.path.append("..")

from .database import Base
from .. import constants


class Job(Base):
    __tablename__ = "jobs"

    # -- Allow updating table schema
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    jobid = Column(String, primary_key=False, unique=True, index=True)
    rqjobid = Column(String, unique=True, index=True)
    jobtype = Column(String)
    queuename = Column(String)
    status = Column(String)#, default=constants.STATUS_QUEUED)
    args = Column(String)
    createdat = Column(DateTime)#, default=dt.datetime.now())
    startedat = Column(DateTime)
    finishedat = Column(DateTime)
    jobinfo = Column(String)
    error = Column(String)
    result = Column(String)
    # waittime = Column(Interval)
    # runtime = Column(Interval)
