# -*- coding: utf-8 -*-
#
import requests
from redis_access import write_items_to_datastore, ping
from settings import DOMAINS_MOST_RECENT, DOMAINS_INTERVAL, DOMAINS_URL
from settings import TOPPAGES_PING
from pycron import PyCron

session=requests.Session()

"""

    Check the domains available for toppages,
    and make those domains available.

    Assume that the available domains can change,
    and that complete coverage is desirable.

    Also assume that there could be many thousands of domains.

    The interval for how often to check for new and/or dropped domains,
    DOMAINS_INTERVAL, is set settings.py

    Given the way available domains are currently delivered,
    this script is designed to run on a single machine.

"""


def get_available_domains():
    r = session.get(DOMAINS_URL)
    return r.json()


def domains_worker():
    domains = get_available_domains()
    write_items_to_datastore(DOMAINS_MOST_RECENT, domains)
    ping(TOPPAGES_PING)


def main():
    cron = PyCron()
    cron.setup(DOMAINS_INTERVAL, domains_worker)
    cron.run()

if __name__ == "__main__":
    main()








