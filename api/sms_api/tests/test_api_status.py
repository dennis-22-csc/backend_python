"""This module tests the end point for getting the status of the sms api.
"""

import unittest
import json
from v1.messages.app import app


class StatusTest(unittest.TestCase):
    """This tests the status endpoint."""
    def setUp(self):
        """Initializes external dependencies"""
        self.app = app.test_client()
    
    def test_status_endpoint(self):
        """Tests the status endpoint."""
        response = self.app.get('/v1/messages/status')
        self.assertEqual(response.status_code, 200)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response_data_dict, {"status":"OK"})
