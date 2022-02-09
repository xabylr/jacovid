#!/usr/bin/env python
import logging

import redis
from rq import Connection, Queue, SimpleWorker

from config import environment
from jobs import refresh_data
from persistence.utils import queries

logging.basicConfig(format='%(asctime)s- %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger()

listen = ['high', 'default', 'low']

conn = redis.from_url(environment.REDIS_URL)


def start_worker():
    """Connect to the database and start listening works in redis"""

    # Check if database is empty for populating places
    if queries.is_database_empty():
        logger.info("Database is empty, populating places and first measures")
        refresh_data.populate_places()
    elif environment.REFRESH_AT_STARTUP:
        logger.info("Existing database detected, retrieving measures for today")
        refresh_data.pull_measures()

    with Connection(conn):
        worker = SimpleWorker(map(Queue, listen))
        worker.work()


if __name__ == '__main__':
    start_worker()
