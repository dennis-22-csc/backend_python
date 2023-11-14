"""This module tests the end point for sending sms in the sms api.
"""

import unittest
import json
from v1.messages.app import app


class SendSmsTest(unittest.TestCase):
    """This tests the send sms endpoint."""
    def setUp(self):
        """Initializes external dependencies"""
        self.app = app.test_client()
    
    def test_send_sms_endpoint_when_to_not_valid_e164(self):
        """Tests the send sms endpoint when to doesn't contain a valid e164 phone number."""
        pay_load = {"to": ["2"], "message": "hey there"}
        response = self.app.post('/v1/messages/sms', json=pay_load)
        self.assertEqual(response.status_code, 201)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        response_data_dict_item_length = len(response_data_dict["messages"])
        self.assertEqual(response_data_dict_item_length, 1)
        response_data_dict_item_delivery_status = response_data_dict["messages"][0]["deliveryStatus"]
        self.assertEqual(response_data_dict_item_delivery_status, "NotDelivered")
    
    def test_send_sms_endpoint_when_to_is_valid_e164(self):
        """Tests the send sms endpoint when to contains a valid e164 number."""
        pay_load = {"to": ["+5018105654558"], "message": "hey there"}
        response = self.app.post('/v1/messages/sms', json=pay_load)
        self.assertEqual(response.status_code, 201)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        response_data_dict_item_length = len(response_data_dict["messages"])
        self.assertEqual(response_data_dict_item_length, 1)
        response_data_dict_item_delivery_status = response_data_dict["messages"][0]["deliveryStatus"]
        self.assertEqual(response_data_dict_item_delivery_status, "DeliveredToNetwork")
        
    def test_send_sms_endpoint_when_to_has_list_inside_list(self):
        """Tests the send sms endpoint when to has list inside list."""
        pay_load = {"to": [[2]], "message": "hey there"}
        response = self.app.post('/v1/messages/sms', json=pay_load)
        self.assertEqual(response.status_code, 400)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 400)
        self.assertEqual(response_data_dict["reason"], "Bad Request")
        self.assertEqual(response_data_dict["message"], "The value of the 'to' field must be a list containing at least one string of phone numbers.")
        
    def test_send_sms_endpoint_when_to_is_number(self):
        """Tests the send sms endpoint when to is number."""
        pay_load = {"to": 5018105654558, "message": "hey there"}
        response = self.app.post('/v1/messages/sms', json=pay_load)
        self.assertEqual(response.status_code, 400)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 400)
        self.assertEqual(response_data_dict["reason"], "Bad Request")
        self.assertEqual(response_data_dict["message"], "The value of the 'to' field must be a list containing at least one phone number.")
        
    def test_send_sms_endpoint_when_to_is_empty_string_list(self):
        """Tests the send sms endpoint when to is empty string list."""
        pay_load = {"to": [""], "message": "hey there"}
        response = self.app.post('/v1/messages/sms', json=pay_load)
        self.assertEqual(response.status_code, 400)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 400)
        self.assertEqual(response_data_dict["reason"], "Bad Request")
        self.assertEqual(response_data_dict["message"], "The value of the 'to' field must be a list containing at least one phone number.")
        
    def test_send_sms_endpoint_when_to_is_empty_list(self):
        """Tests the send sms endpoint when to is empty list."""
        pay_load = {"to": [], "message": "hey there"}
        response = self.app.post('/v1/messages/sms', json=pay_load)
        self.assertEqual(response.status_code, 400)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 400)
        self.assertEqual(response_data_dict["reason"], "Bad Request")
        self.assertEqual(response_data_dict["message"], "The 'to' and 'message' fields must not contain empty values.")
        
    def test_send_sms_endpoint_when_no_to(self):
        """Tests the send sms endpoint when there is no to."""
        pay_load = {"me": ["+5018105654558"], "message": "hey there"}
        response = self.app.post('/v1/messages/sms', json=pay_load)
        self.assertEqual(response.status_code, 400)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 400)
        self.assertEqual(response_data_dict["reason"], "Bad Request")
        self.assertEqual(response_data_dict["message"], "The 'to' and 'message' fields are required in the request body.")
        
    def test_send_sms_endpoint_when_message_is_not_string(self):
        """Tests the send sms endpoint when message is not string."""
        pay_load = {"to": ["+5018105654558"], "message": ["hey there"]}
        response = self.app.post('/v1/messages/sms', json=pay_load)
        self.assertEqual(response.status_code, 400)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 400)
        self.assertEqual(response_data_dict["reason"], "Bad Request")
        self.assertEqual(response_data_dict["message"], "The value of the 'message' field must be a string.")  
  
