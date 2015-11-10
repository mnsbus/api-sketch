
import redis
from settings import HOSTNAME


redis_config = {
        'host': HOSTNAME, # TODO: host selection
        'port': 6379, # TODO: port selection
        'db': 0, # TODO: db selection
}

# TODO: this needs to be application-wide to be safe
rc = redis.StrictRedis(**redis_config)


def get_pubsub(channel):
    pubsub = rc.pubsub()
    pubsub.subscribe([channel])
    return pubsub


def pop_n_items(key, n):
    #pipe = rc.pipeline()
    domains = []
    for i in xrange(n):
        d = rc.spop(key)
        if d:
           domains.append(d)
    #domains = pipe.lrange(DOMAINS_AVAILABLE, 0, DOMAINS_MAX_PER_CHANNEL)
    #pipe.ltrim(DOMAINS_AVAILABLE, 0, DOMAINS_MAX_PER_CHANNEL)
    #pipe.execute()
    return domains


def ping(key):
    rc.publish(key, 'true')


def write_items_to_datastore(key, items):
    #pipe = rc.pipeline()
    for item in items:
        if item:
            rc.sadd(key, item)
            #if not pipe.ismember(key, item):
            #    pipe.rpush(DOMAINS_AVAILABLE, domain)
    #pipe.execute()





