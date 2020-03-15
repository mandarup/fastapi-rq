import argparse
from redis import Redis
from rq import Queue
import rq
import logging
import pprint
import os
import uuid
import json
from collections.abc import Mapping

from . import task_config
# from .database import db
from . import database
from .database import crud, models, schemas


logging.basicConfig(
    format=
    '%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_parser():
    parser = argparse.ArgumentParser(
        description="Job Queue",
        epilog="",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-q",
        "--queuename",
        dest='queuename',
        help="Name of rq queue to use")
    parser.add_argument("-j",
                        "--jobtype",
                        dest='jobtype',
                        help="A predefined type of job",
                        choices=['testtask'],
                        required=True)
    parser.add_argument("-a",
        "--jobargs",
        # dest='jobargs',
        type=str,
        help="job args")
    return parser





def run_one_job(cmd):
    import subprocess
    output = subprocess.run(cmd,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True,
                            #capture_output=True,
                            )
    logger.critical(f'Subprocess output: {output}')
    # os.system(cmd)
    return output


async def submit_with_args(args):
    logger.setLevel('DEBUG')
    argslist = []
    for k, v in args.items():
        #-- if value is dict, convert to string
        if isinstance(v, Mapping):
            v = json.dumps(v)

        # -- prepend `--` to the keys to match argparse
        k = '--' + k
        argslist.extend([k, v])

    logger.debug(f'Raw args: {args}')
    logger.debug(f'List args: {argslist}')
    parsedargs = get_parser().parse_args(argslist)
    logger.debug(f'Parsed args: {parsedargs}')

    redis_con = Redis(port='6379', host='redis')

    queuename = parsedargs.queuename
    logger.info(f'submitting to queue: {queuename}')
    q = Queue(queuename, connection=redis_con)

    # -- process job args
    jobargs = json.loads(parsedargs.jobargs)
    logger.debug(f'jobargs: {jobargs}')
    script_args = []
    for k,v in jobargs.items():
        if isinstance(v, Mapping):
            # -- separate key-value pairs with ':'
            v =  ' '.join([f'{k1}={v1}' for k1,v1 in v.items()])

        elif isinstance(v, list):
            # -- convert list items to string of space separated values
            # -- Argparse has good support for list args
            v = ' '.join(v)
        script_args.extend([k, v])

    logger.debug(f'script_args: {script_args}')
    # -- convert script args to single string
    script_args = ' '.join(script_args)

    sep = ' '
    cmd = task_config.tasks[parsedargs.jobtype] + sep + script_args
    logger.info(f'command: {cmd}')

    #-- add rqjobid to the cmd to pass the id to the worker
    jobid = uuid.uuid4().hex
    cmd += f' --rqjobid {jobid}'

    # -- Now that we have a jobid, create a db entry
    db = database.get_db()
    job = schemas.Job(jobid=None,
                      queuename=parsedargs.queuename,
                      jobtype=parsedargs.jobtype,
                      rqjobid=jobid,
                      args=cmd)
    crud.create_job(db, job)

    logger.info(f'submitting cmd: {cmd}')
    # -- Create rq-job, predefining job id with the one we just created
    job = rq.job.Job.create(
        run_one_job,
        # kwargs={'rqjobid': jobid},
        args=(cmd, ),
        # job_timeout='48h',
        result_ttl=172800,  #60s * 60m * 24h * 2d,  # result deleted after 2 days
        failure_ttl=172800,
        id=jobid, # Manually assigning job id
        description=cmd,
        connection=redis_con,
        timeout='48h',
        ttl='72h'
    )
    logger.debug(f'Job id: {job.id}')
    logger.debug(f'Job: {job}')
    q.enqueue_job(job)

    logging.info(f'queuing output: {pprint.pformat(job)}')

    return job



if __name__ == '__main__':
    submit()
