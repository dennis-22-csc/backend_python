"""This module tests the end point for sending sms in the sms api.
"""

import unittest
import json
from v1.messages.app import app
from v1.oauth.views.utils import delete_obj
from models.access_token import AccessToken
from parameterized import parameterized
from unittest.mock import patch, Mock, MagicMock

class SendSmsTest(unittest.TestCase):
    """This tests the send sms endpoint."""
    def setUp(self):
        """Initializes external dependencies"""
        self.app = app.test_client()
        self.token = "746341xrghqwsb"
        self.header = {'Authorization': self.token}
    
    @parameterized.expand([
    	({"to": ["2"], "message": "hey there"}, 201, 1, ["NotDelivered"]),
    	({"to": ["+5018105654558"], "message": "hey there"}, 201, 1, ["DeliveredToNetwork"]),
    	({"to": ["2", "+5018105654558"], "message": "hey there"}, 201, 2, ["NotDelivered", "DeliveredToNetwork"]),
    ])
    @patch('v1.messages.views.index.delete_obj')
    @patch('v1.messages.views.index.has_expired')
    @patch('v1.messages.views.index.validate_token')
    def test_send_sms_endpoint_phone_numbers(self, pay_load, expected_code, expected_length, expected_delivery_status, mock_validate_token, mock_has_expired, mock_delete_obj):
        """Tests the send sms endpoint when to doesn't contain a valid e164 phone number."""
        token_obj_mock = Mock(spec=AccessToken)
        mock_validate_token.return_value = token_obj_mock
        mock_has_expired.return_value = False
        response = self.app.post('/v1/messages/sms', json=pay_load, 
headers=self.header)
        mock_validate_token.assert_called_once()
        mock_validate_token.assert_called_once_with(self.token)
        mock_has_expired.assert_called_once()
        mock_has_expired.assert_called_once_with(token_obj_mock)
        self.assertEqual(response.status_code, expected_code)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        response_data_dict_item_length = len(response_data_dict["messages"])
        self.assertEqual(response_data_dict_item_length, expected_length)
        for i in range(len(response_data_dict["messages"])):
            response_data_dict_item_delivery_status = response_data_dict["messages"][i]["deliveryStatus"]
            self.assertEqual(response_data_dict_item_delivery_status, expected_delivery_status[i])
     
     
    @parameterized.expand([
    	({"to": [[2]], "message": "hey there"}, 400,  "Bad Request",  "The value of the 'to' field must be a list containing at least one string of phone numbers.", ),
    	({"to": 5018105654558, "message": "hey there"},  400,  "Bad Request", "The value of the 'to' field must be a list containing at least one phone number."),
    	({"to": [""], "message": "hey there"},  400,  "Bad Request", "The value of the 'to' field must be a list containing at least one phone number."),
    	({"to": [], "message": "hey there"}, 400,  "Bad Request", "The 'to' and 'message' fields must not contain empty values.", ),
    	({"me": ["+5018105654558"], "message": "hey there"}, 400,  "Bad Request", "The 'to' and 'message' fields are required in the request body."),
    	({"to": ["+5018105654558"], "message": ["hey there"]},  400,  "Bad Request", "The value of the 'message' field must be a string."),
    	({"to": ["+5018105654558"], "message": "hey there", "name": "Dennis"}, 400,  "Bad Request", "You can't have more than two fields in the request json."),
    ])
    @patch('v1.messages.views.index.delete_obj')
    @patch('v1.messages.views.index.has_expired')
    @patch('v1.messages.views.index.validate_token')
    def test_send_sms_endpoint_bad_requests(self, pay_load, expected_code, expected_reason, expected_message, mock_validate_token, mock_has_expired, mock_delete_obj):
        """Tests endpoint for bad requests."""
        token_obj_mock = Mock(spec=AccessToken)
        mock_validate_token.return_value = token_obj_mock
        mock_has_expired.return_value = False
        response = self.app.post('/v1/messages/sms', json=pay_load, headers=self.header)
        mock_validate_token.assert_called_once()
        mock_validate_token.assert_called_once_with(self.token)
        mock_has_expired.assert_called_once()
        mock_has_expired.assert_called_once_with(token_obj_mock)
        self.assertEqual(response.status_code, expected_code)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], expected_code)
        self.assertEqual(response_data_dict["reason"], expected_reason)
        self.assertEqual(response_data_dict["message"], expected_message) 

    @parameterized.expand([
    	("no_token", {"to": ["+5018105654558"], "message": "hey there"}, 401, "Unauthorized", "Please provide an access token."),
    	("invalid_token", {"to": ["+5018105654558"], "message": "hey there"}, 401, "Unauthorized", "Please provide a valid access token."),
    ("expired_token", {"to": ["+5018105654558"], "message": "hey there"}, 401, "Unauthorized", "Access token has expired."),
    ])
    @patch('v1.messages.views.index.delete_obj')
    @patch('v1.messages.views.index.has_expired')
    @patch('v1.messages.views.index.validate_token')
    def test_send_sms_endpoint_token(self, case_name, pay_load, expected_code, expected_reason, expected_message, mock_validate_token,mock_has_expired, mock_delete_obj):
        """Test endpoint for token associated edge cases"""
        response = None
        if case_name == "no_token":
            response = self.app.post('/v1/messages/sms', json=pay_load)
            mock_validate_token.assert_not_called()
        elif case_name == "invalid_token":
            mock_validate_token.return_value = None
            response = self.app.post('/v1/messages/sms', json=pay_load, headers=self.header)
            mock_validate_token.assert_called_once()
            mock_validate_token.assert_called_once_with(self.token)
        elif case_name == "expired_token":
            token_obj_mock = Mock(spec=AccessToken)
            mock_validate_token.return_value = token_obj_mock
            mock_has_expired.return_value = True
            response = self.app.post('/v1/messages/sms', json=pay_load, headers=self.header)
            mock_validate_token.assert_called_once()
            mock_validate_token.assert_called_once_with(self.token)
            mock_has_expired.assert_called_once()
            mock_has_expired.assert_called_once_with(token_obj_mock)
        self.assertEqual(response.status_code, expected_code)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], expected_code)
        self.assertEqual(response_data_dict["reason"], expected_reason)
        self.assertEqual(response_data_dict["message"], expected_message)
        
    
    
