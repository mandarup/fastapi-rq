import os
import time
import logging
logger = logging.getLogger(__name__)

def run_one_job(cmd): 
   os.system(cmd)


def dummy_job(wait):
   print(f'runing job for {wait}')
   time.sleep(wait)


def dummy_job2(args, runtime=None, dummy=True):
   import time
   logger.info(f'received arg: {runtime}')
   time.sleep(10)