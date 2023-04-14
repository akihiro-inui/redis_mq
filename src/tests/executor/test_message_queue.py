import os
import sys

sys.path.insert(0, os.getcwd())
import unittest
from src.scheduler import MessageQueue
from rq import push_connection


class TestMessageQueue(unittest.TestCase):
    """
    Tests message queue
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.MQ = MessageQueue()

    def test_01_connect_to_redis(self):
        # Create connection to Redis
        redis_connection = self.MQ.get_connection()
        push_connection(redis_connection)

    def test_02_create_queue(self):
        # Create test queue
        queue = self.MQ.create_queue("test_queue")
        self.assertIsNotNone(queue)

    def test_03_enqueue_job_and_check(self):
        # Create test task, enqueue it and check if job ID is returned
        def _sort(array):
            return array.sorted()

        # Create test queue
        queue = self.MQ.create_queue("test_queue")

        # Enqueue the job
        result = self.MQ.enqueue_job(queue, _sort, [1, 2])
        self.assertIsNotNone(result)

        # Get Job ID
        job_id = result.get_id()
        self.assertIsNotNone(job_id)

        # Check job status
        status = self.MQ.get_job_status(queue, job_id)
        self.assertEqual("queued", status._status)

    def test_04_get_all_job_status(self):
        # Create test queue, get status of all jobs
        queue = self.MQ.create_queue("test_queue")
        all_job_status = self.MQ.get_all_job_status(queue)
        self.assertIsNotNone(all_job_status)
