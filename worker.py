from redis import Redis
from rq import Queue, Worker

conn = Redis('127.0.0.1', 6379)
q = Queue("Queue", connection=conn)

if __name__ == '__main__':
    Worker([q], connection=conn).work()
