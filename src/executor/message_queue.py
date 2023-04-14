import os
import sys

sys.path.insert(0, os.getcwd())

from redis import Redis
from rq import Queue, Retry
from typing import List
from src.utils.types import QueuedValue


class MessageQueue:
    def __init__(self) -> None:
        # Initiate Redis connector
        self.redis_host = os.environ.get("REDIS_HOST", "localhost")
        self.redis_port = os.environ.get("REDIS_PORT", "6379")

    def get_connection(self):
        return Redis(host=self.redis_host, port=self.redis_port, db=0)

    def create_queue(self, name: str = "queue") -> Queue:
        """
        Create a message queue
        :return: queue
        """
        return Queue(connection=self.get_connection(), name=name)

    @staticmethod
    def enqueue_job(queue: Queue, task_function, input_value: QueuedValue):
        """
        Given queue, input value and task function, enqueue the job.
        Retry 3 times with 60 seconds interval if it fails.
        :param queue: Queue class with name
        :param: task_function: Function (job) to be executed
        :param input_value: Input value
        :return: Result of the queueing task
        """
        return queue.enqueue(
            task_function, input_value.array, retry=Retry(max=3, interval=60)
        )

    @staticmethod
    def enqueue_dependent_jobs(queue: Queue,
                              first_task_function,
                              second_task_function,
                              input_value: List[int]):
        """
        Given queue, enqueue the jobs with input value.
        Retry 3 times with 60 seconds interval if it fails.
        :param queue: Queue class with name
        :param first_task_function: First function (job) to be executed
        :param second_task_function: Second function (job) to be executed
        :param input_value: Input value
        :return: Result of the queueing jobs
        """
        fist_job = queue.enqueue(first_task_function, input_value, retry=Retry(max=3, interval=60))
        second_job = queue.enqueue(second_task_function, depends_on=fist_job, retry=Retry(max=3, interval=60))
        return second_job

    @staticmethod
    def get_job_status(queue: Queue, job_id: str):
        """
        Given queue and job ID, return the status and it's value (if the job is already finished)
        :param queue: Queue class with name
        :param job_id: Job ID (UUID)
        :return: Status of the job
        """
        return queue.fetch_job(job_id)

    def get_all_job_status(self, queue: Queue) -> List[dict]:
        """
        Get all job IDs stored in Redis and their status and store them into a list
        :param queue: the queue to check the jobs
        :return: List of the job IDs and their status etc. [{"job_id": UUID, "status": "finished"}]
        """
        all_jobs = []
        # Get all finished jobs
        for finished_job_id in queue.finished_job_registry.get_job_ids():
            all_jobs.extend([{"status": "finished", "job_id": finished_job_id}])

        # Get all failed jobs
        for failed_job_id in queue.failed_job_registry.get_job_ids():
            all_jobs.extend([{"status": "failed", "job_id": failed_job_id}])

        # Get all queuing jobs
        for queued_job_id in queue.get_job_ids():
            all_jobs.extend([{"status": "queued", "job_id": queued_job_id}])

        return all_jobs
