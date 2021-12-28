#!/usr/bin/env python
import sys
import config.environment as env
import redis
from rq import Queue
from jobs.refresh_data import pull_measures

conn = redis.from_url(env.REDIS_URL)
q = Queue(connection=conn)

if __name__ == '__main__':
    try:
        command = sys.argv[1]
    except IndexError as e:
        print("Missing task argument")
        sys.exit()
    
    if command == "pull_measures":
        q.enqueue(pull_measures)
    else:
        print(f'Unrecognized command {command}')

    

