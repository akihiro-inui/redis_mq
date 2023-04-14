import os
import sys

sys.path.insert(0, os.getcwd())

from rq import Worker, Queue, get_current_job
from typing import List
from src.executor import MQ, queue


class CustomWorker:
    @staticmethod
    def create_worker(queue: Queue, redis_connection):
        """
        Creates a worker and register it to Redis
        """
        return Worker([queue], connection=redis_connection)

    @staticmethod
    def sort_array(input_array: List[int]):
        """
        Executes the job, in this function, it sorts the array
        """
        return sorted(input_array)

    @staticmethod
    def take_first_value_from_array():
        """
        Get the finished job result, take out the first number from the array and return it
        """
        current_job = get_current_job(MQ.get_connection())
        first_job_id = current_job.dependency.get_id()
        sorted_array = MQ.get_job_status(queue, first_job_id).result
        return sorted_array[0]


if __name__ == "__main__":
    queue = MQ.create_queue()
    CW = CustomWorker()
    WK = CW.create_worker(queue, MQ.get_connection())
    WK.work()
