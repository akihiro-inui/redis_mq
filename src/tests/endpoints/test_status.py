import os
import sys

sys.path.insert(0, os.getcwd())
import unittest
from fastapi.testclient import TestClient

from src.main import app


class TestStatusEndpoint(unittest.TestCase):
    """
    Tests status endpoint with the test API client
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = TestClient(app)

    def test_01_get_status_healthy(self):
        response = self.client.get("/status")
        response_json = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual("OK", response_json.get("status"))
