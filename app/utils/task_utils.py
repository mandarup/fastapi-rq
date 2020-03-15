
import logging
from typing import List

logger = logging.getLogger(__name__)


def split_rqjobid(args:str) -> List:
    logger.setLevel('DEBUG')
    logger.info(f'Args recieved by job: {args}')
    argslist = None
    rqjobid = None
    if args is not None:
        if not isinstance(args, list):
            argslist = args.split()
        else:
            argslist = args
        try:
            rqjobid_index = argslist.index("--rqjobid")
            # first remove the key, only need the value
            argslist.pop(rqjobid_index)
            rqjobid = argslist.pop(rqjobid_index)
            logger.info(f'RQ Job ID: {rqjobid}')

        except ValueError:
            pass

    if rqjobid is None:
        logger.error("rqjobid cannot be NoneType")
        raise Exception("rqjobid cannot be NoneType")
    return argslist, rqjobid
