import os
import sys

sys.path.insert(0, os.getcwd())
import unittest
from src.scheduler import MessageQueue
from src.scheduler.worker import CustomWorker


class TestWorker(unittest.TestCase):
    """
    Tests Worker
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.MQ = MessageQueue()
        self.WK = CustomWorker()

    def test_01_create_worker(self):
        # Create test worker
        queue = self.MQ.create_queue("test_queue")
        worker = self.WK.create_worker(queue, self.MQ.get_connection())
        self.assertIsNotNone(worker)

    def test_02_test_job(self):
        # Create test job
        test_array = [1, 4, 5, 2]
        result = self.WK.create_job(test_array)
        self.assertEqual([1, 2, 4, 5], result)
