#!/usr/bin/env python
import logging
import config.environment as env
import persistence.database as db
import jobs.refresh_data as refresh_data
import persistence.utils.queries as queries
import redis
from rq import Worker, Queue, Connection


logging.basicConfig(format='%(asctime)s- %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger()

listen = ['high', 'default', 'low']

conn = redis.from_url(env.REDIS_URL)

def start_worker():
    """Connect to the database and start listening works in redis"""

    # Establish a session with database
    db.connect(env.DB_URL, env.DEBUG)

    # Check if database is empty for populating places
    if queries.is_database_empty():
        logger.info("Database is empty, populating places and first measures")
        refresh_data.populate_places(insert_measures=True)
    else:
        logger.info("Existing database detected, retrieving measures for today")
        refresh_data.pull_measures()

    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()


if __name__ == '__main__':
    start_worker()
