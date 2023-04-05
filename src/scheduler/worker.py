import os
import sys

sys.path.insert(0, os.getcwd())

from typing import List
from rq import Worker, Queue
from src.scheduler import MQ


class CustomWorker:
    def create_worker(self, queue: Queue, redis_connection):
        return Worker([queue], connection=redis_connection)

    @staticmethod
    def create_job(input_array: List[int]):
        return sorted(input_array)


if __name__ == "__main__":
    queue = MQ.create_queue()
    CW = CustomWorker()
    WK = CW.create_worker(queue, MQ.get_connection())
    WK.work()
