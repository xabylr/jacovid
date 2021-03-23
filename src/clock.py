#!/usr/bin/env python
import config.environment as env
from apscheduler.schedulers.blocking import BlockingScheduler
import redis
from rq import Queue
from jobs.refresh_data import pull_measures

conn = redis.from_url(env.REDIS_URL)

q = Queue(connection=conn)

sched = BlockingScheduler()


@sched.scheduled_job('interval', hours=3, )
def periodical_job():
    q.enqueue(pull_measures)


def start_clock():
    """Start the clock"""
    sched.start()


if __name__ == '__main__':
    start_clock()
