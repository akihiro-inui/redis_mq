import os
import sys

sys.path.insert(0, os.getcwd())
import unittest
from fastapi.testclient import TestClient

from src.main import app


class TestSchedulerEndpoint(unittest.TestCase):
    """
    Tests scheduler endpoints with the test API client
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = TestClient(app)

    def test_01_get_all_jobs_without_any(self):
        """Check if querying the empty jobs works"""
        response = self.client.get("/jobs")
        self.assertEqual(200, response.status_code)

    def test_02_create_job(self):
        """Create job, check the response"""
        request_body = {"array": [0, 4, 1, 3]}

        # Send API request with unsorted array
        response = self.client.post("/register_job", json=request_body)
        response_json = response.json()

        # Check response
        self.assertEqual(201, response.status_code)
        self.assertEqual("Successfully enqueued the job", response_json.get("message"))

    def test_03_create_job_with_wrong_input_data_type(self):
        """Create job, check the response"""
        request_body = {"array": "Test String"}

        # Send API request with unsorted array
        response = self.client.post("/register_job", json=request_body)
        response_json = response.json()

        # Check response
        self.assertEqual(422, response.status_code)

    def test_04_create_job_and_check_status(self):
        """Create job, check the status"""
        request_body = {"array": [0, 4, 1, 3]}

        # Send API request with unsorted array
        response = self.client.post("/register_job", json=request_body)
        response_json = response.json()
        self.assertEqual(201, response.status_code)
        job_id = response_json["job_id"]

        # Check job status by job ID
        response = self.client.get(f"/jobs/{job_id}")
        response_json = response.json()
        self.assertEqual(200, response.status_code)
        self.assertEqual(response_json["job_id"], job_id)
        self.assertIn(response_json["job_status"], ["queued", "finished"])
        self.assertIsNotNone(response_json["enqueued_at"])
        self.assertEqual(
            "Successfully retrieved the requested job status",
            response_json.get("message"),
        )

    def test_05_get_all_jobs(self):
        """Check if querying the empty jobs works"""
        response = self.client.get("/jobs")
        response_json = response.json()
        self.assertEqual(200, response.status_code)
        self.assertGreaterEqual(len(response_json["jobs"]), 1)
        self.assertEqual(
            "Successfully retrieved all jobs status", response_json.get("message")
        )
