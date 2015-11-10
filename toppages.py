
import urlparse
import grequests # uses gevent
from redis_access import get_pubsub, ping, pop_n_items, write_items_to_datastore
from settings import ACCELERANDS_DOMAINS, ACCELERANDS_PING
from settings import APIKEY, MAX_PROCESSES
from settings import DOMAINS_MOST_RECENT, DOMAINS_MAX_PER_CHANNEL
from settings import TOPPAGES_BASE_URL, TOPPAGES_PAGE_LIMIT, TOPPAGES_PING
from sql_access import write_toppage_records
from utils import create_epoch_timestamp

"""

    Hits toppages server after a ping from the producer.
    conceptually, assumes some kind of distributed datastore
    (NOT redis + 'localhost' as given in settings.py !)

"""


def make_toppages_payload(domain):
    """Grequests and Toppages-specific helper function """
    return {'apikey': APIKEY, 'host': domain, 'limit': TOPPAGES_PAGE_LIMIT}


def get_domain_from_query_string(url):
    """Extracts the Mongo-friendly domain and suffix from the query string"""
    parsed = urlparse.urlparse(url)
    host = urlparse.parse_qs(parsed.query)['host'][0]
    return host


def make_async_requests(domains):
    """Uses the gevent-based grequests library to make async requests"""
    # TODO: better way to use requests with gevent? or better library?
    # grequests is no longer maintained
    # it eventually locks up
    rs = []
    for domain in domains:
        params = make_toppages_payload(domain)
        rs.append(grequests.get(TOPPAGES_BASE_URL, params=params))
    results = grequests.map(rs) # for throttling: size=DOMAINS_MAX_PER_CHANNEL
    return results


def process_article(a, domain, timestamp):
    a['domain'] = domain
    a['timestamp'] = timestamp
    if not a['path'].startswith("/"):
        a['path'] = "/" + a['path']
    return a


def process_async_response(r, timestamp):
    domain = get_domain_from_query_string(r.url)
    articles = r.json()
    articles = [process_article(a, domain, timestamp) for a in articles if a]
    return articles


def process_async_responses(results):
    """Adds consistent timestamp to toppages responses"""
    # TODO: find more accurate way to timestamp each response
    # Better to pull out of response object
    timestamp = create_epoch_timestamp()
    docs = []
    for r in results:
        if r.status_code == 200:
            docs.extend(process_async_response(r, timestamp))
    return docs


def toppages_worker(domains):
    responses = make_async_requests(domains)
    documents = process_async_responses(responses)
    write_toppage_records(documents)
    write_items_to_datastore(ACCELERANDS_DOMAINS, domains)


def main():
    pubsub = get_pubsub(TOPPAGES_PING)
    for notification in pubsub.listen():
        domains = pop_n_items(DOMAINS_MOST_RECENT, DOMAINS_MAX_PER_CHANNEL)
        print domains
        # TODO: split domains among threads/processes & launch
        toppages_worker(domains)
        ping(ACCELERANDS_PING)


if __name__ == "__main__":
    main()
