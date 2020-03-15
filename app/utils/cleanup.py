import logging
import redis


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

r = redis.StrictRedis()
 
 
def purgeq(r, qname):
    while True:
        logger.info(f'deleting: {qname}')
        jid = r.lpop(qname)
        if jid is None:
            break

        r.delete("rq:job:" + jid)
        logger.info(f'deleted: {jid}')


def main():
    import sys
    args = sys.argv[1:]
    logger.info(args)
    print(args)
    purgeq(r, args[0])

if __name__ == '__main__':
    main()