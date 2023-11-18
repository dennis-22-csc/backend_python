# test_api_client.py

import unittest
from unittest.mock import patch
from api_client import APIClient

class TestAPIClient(unittest.TestCase):

    @patch('api_client.requests.get')
    def test_different_responses(self, mock_get):
        # Set up the side_effect to return different responses
        mock_responses = [
            {'status': 'success', 'data': [1, 2, 3]},
            {'status': 'error', 'message': 'Internal Server Error'},
            {'status': 'success', 'data': [4, 5, 6]}
        ]
        mock_get.side_effect = mock_responses

        # Create an instance of the class under test
        api_client = APIClient()

        # Call the method under test multiple times
        result1 = api_client.get_data()
        result2 = api_client.get_data()
        result3 = api_client.get_data()

        # Assertions
        self.assertEqual(result1, {'status': 'success', 'data': [1, 2, 3]})
        self.assertEqual(result2, {'status': 'error', 'message': 'Internal Server Error'})
        self.assertEqual(result3, {'status': 'success', 'data': [4, 5, 6]})

        # Check how many times the mock was called
        self.assertEqual(mock_get.call_count, 3)
