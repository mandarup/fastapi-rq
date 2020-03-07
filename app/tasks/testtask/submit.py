import logging
import os
import sys
import datetime as dt
import time



from ... import database
from ...database import models
from ... import constants
from ...utils import task_utils


logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')






def submit(args):


    argslist, rqjobid = task_utils.split_rqjobid(args)
    logger.info(f'Received args: {argslist} for rqjobid {rqjobid}')
    run_id = str(time.time())
    jobinfo = 'test job'

    db = database.get_db()
    db.query(models.Job).filter(models.Job.rqjobid == rqjobid).update({
        models.Job.startedat:
        dt.datetime.now(),
        models.Job.jobid:
        run_id,
        models.Job.status:
        constants.STATUS_RUNNING,
        models.Job.jobinfo: jobinfo,
    })
    db.commit()

    time.sleep(10)

    db = database.get_db()
    db.query(models.Job).filter(models.Job.rqjobid == rqjobid).update({
        # models.Job.startedat:dt.datetime.now(),
        # models.Job.jobid: run_id,
        models.Job.status: constants.STATUS_SUCCEEDED,
        # models.Job.jobinfo: jobinfo,
    })
    db.commit()





if __name__ == '__main__':
    import json
    import pprint
    import argparse

    args = sys.argv[1:]
    logger.setLevel('DEBUG')
    logger.info(f'Received args: {args}')
    submit(args)
