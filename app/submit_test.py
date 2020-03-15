import argparse
from redis import Redis
from rq import Queue
import logging
import pprint


logger = logging.getLogger(__name__)

def parse_args():
    
    epilog = """How to setup supervisor and rq:
    Create a file 'supervisord.conf' with the following contents:

        [program:rqworker]
        command=/home/sjp/.virtualenvs/analytics/bin/rq worker databricks
        process_name=rqworker_%(process_num)s
        numprocs=50

    (change contents to whatever suits your installation)
    Then you can run 'supervisord -n' to create 50 rq workers (note:
    the '-n' option makes supervisor to run in the foreground)
    Then call this program to give work to the rq worker nodes.
    """

    parser = argparse.ArgumentParser(
        description="Run many databricks jobs at once",
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-q",
        dest='queuename',
        default='long',
        help="Name of rq queue to use (default is 'databricks')")

    parser.add_argument("-n",
        dest='numjobs',
        default=5,
        type=int,
        help="Number of jobs")

    # parser.add_argument("-c",
    #     dest='companyfile',
    #     required=True,
    #     help="Name of file containing company names (one per line)")

    # parser.add_argument("script_to_run",
    #     nargs=1,
    #     help="Name of script to run. Must accept as argument the company name")

    args = parser.parse_args()

    # -- create a dict out of args
    # opts = copy.copy(vars(arg))
    return args



def submit():
    logging.getLogger().setLevel(logging.INFO)
    
    # if args['verbose'] >= 1:
    #     logging.getLogger().setLevel(logging.DEBUG)
    f = '%(asctime)-15s %(levelname)-8s %(message)s'
    logging.basicConfig(format=f)

    import runonejob
    print(runonejob.dummy_job)

    args = parse_args()
    jobspec = {'short': 5, 'long': 20,  'default': 10, 'urgent': 20}
    runtime = jobspec[args.queuename]
    kwargs = {'runtime': runtime, 'dummy':False}
        
    redis_con = Redis()

    queue_name = args.queuename
    q = Queue(queue_name, connection=redis_con)
    logger.info(q)
    # runonejob.dummy_job(10)
    
    jobs = {}
    for j in range(args.numjobs):
        logging.info(">>> Queuing %s" % j)
        
        print(f'sleep time: {runtime}')
        # job = q.enqueue(runonejob.dummy_job, runtime,
        #         job_timeout='5h')
        job = q.enqueue('restapp.runonejob.dummy_job', args=(10,),
                job_timeout='5h')

        # job = q.enqueue(runonejob.dummy_job2, kwargs=kwargs,
        #         job_timeout='5h')
        jobs[j] = job
        # logging.info(pprint.pformat(job))

    # logging.info(pprint.pformat(jobs))


def submit_with_args(args):
    logging.getLogger().setLevel(logging.INFO)
    
    # if args['verbose'] >= 1:
    #     logging.getLogger().setLevel(logging.DEBUG)
    f = '%(asctime)-15s %(levelname)-8s %(message)s'
    logging.basicConfig(format=f)


    # import runonejob

    kwargs = args.jobargs
        
    redis_con = Redis()

    queue_name = args.queuename
    print(f'submitting to queue: {queue_name}')
    print(f'submitting njobs: {args.numjobs}')
    q = Queue(queue_name, connection=redis_con)

    
    jobs = {}
    for j in range(int(args.numjobs)):
        logging.info(">>> Queuing %s" % j)
        
        # job = q.enqueue(runonejob.dummy_job, runtime,
        #         job_timeout='5h')

        logging.info(f'kwargs: {kwargs}, {type(kwargs)}')
        job = q.enqueue('restapp.runonejob.dummy_job2', kwargs=kwargs,
                job_timeout='5h')
        jobs[j] = job
        logging.info(pprint.pformat(job))

    # logging.info(pprint.pformat(jobs))





if __name__ == '__main__':
    submit()



