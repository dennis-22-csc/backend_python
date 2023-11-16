"""This module tests the end point for sending sms in the sms api.
"""

import unittest
import json
from v1.messages.app import app
from v1.oauth.views.utils import delete_obj
from models.access_token import AccessToken

class SendSmsTest(unittest.TestCase):
    """This tests the send sms endpoint."""
    def setUp(self):
        """Initializes external dependencies"""
        self.app = app.test_client()
        self.token_obj = generate_token(1000)
        self.token = self.token_obj.access_token
        self.header = {'Authorization': self.token}
    
    def test_send_sms_endpoint_when_to_not_valid_e164(self):
        """Tests the send sms endpoint when to doesn't contain a valid e164 phone number."""
        pay_load = {"to": ["2"], "message": "hey there"}
        
        response = self.app.post('/v1/messages/sms', json=pay_load, 
headers=self.header)
        self.assertEqual(response.status_code, 201)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        response_data_dict_item_length = len(response_data_dict["messages"])
        self.assertEqual(response_data_dict_item_length, 1)
        response_data_dict_item_delivery_status = response_data_dict["messages"][0]["deliveryStatus"]
        self.assertEqual(response_data_dict_item_delivery_status, "NotDelivered")
        delete_obj(self.token_obj)
    
    def test_send_sms_endpoint_when_to_is_valid_e164(self):
        """Tests the send sms endpoint when to contains a valid e164 number."""
        pay_load = {"to": ["+5018105654558"], "message": "hey there"}
        
        response = self.app.post('/v1/messages/sms', json=pay_load, headers=self.header)
        self.assertEqual(response.status_code, 201)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        response_data_dict_item_length = len(response_data_dict["messages"])
        self.assertEqual(response_data_dict_item_length, 1)
        response_data_dict_item_delivery_status = response_data_dict["messages"][0]["deliveryStatus"]
        self.assertEqual(response_data_dict_item_delivery_status, "DeliveredToNetwork")
        delete_obj(self.token_obj)
       
    def test_send_sms_endpoint_when_to_has_list_inside_list(self):
        """Tests the send sms endpoint when to has list inside list."""
        pay_load = {"to": [[2]], "message": "hey there"}
            
        response = self.app.post('/v1/messages/sms', json=pay_load, headers=self.header)
        self.assertEqual(response.status_code, 400)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 400)
        self.assertEqual(response_data_dict["reason"], "Bad Request")
        self.assertEqual(response_data_dict["message"], "The value of the 'to' field must be a list containing at least one string of phone numbers.")
        delete_obj(self.token_obj)

    def test_send_sms_endpoint_when_to_is_number(self):
        """Tests the send sms endpoint when to is number."""
        pay_load = {"to": 5018105654558, "message": "hey there"}
           
        response = self.app.post('/v1/messages/sms', json=pay_load, headers=self.header)
        self.assertEqual(response.status_code, 400)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 400)
        self.assertEqual(response_data_dict["reason"], "Bad Request")
        self.assertEqual(response_data_dict["message"], "The value of the 'to' field must be a list containing at least one phone number.")
        delete_obj(self.token_obj)

    def test_send_sms_endpoint_when_to_is_empty_string_list(self):
        """Tests the send sms endpoint when to is empty string list."""
        pay_load = {"to": [""], "message": "hey there"}
        
        response = self.app.post('/v1/messages/sms', json=pay_load, headers=self.header)
        self.assertEqual(response.status_code, 400)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 400)
        self.assertEqual(response_data_dict["reason"], "Bad Request")
        self.assertEqual(response_data_dict["message"], "The value of the 'to' field must be a list containing at least one phone number.")
        delete_obj(self.token_obj)

    def test_send_sms_endpoint_when_to_is_empty_list(self):
        """Tests the send sms endpoint when to is empty list."""
        pay_load = {"to": [], "message": "hey there"}
        
        response = self.app.post('/v1/messages/sms', json=pay_load, headers=self.header)
        self.assertEqual(response.status_code, 400)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 400)
        self.assertEqual(response_data_dict["reason"], "Bad Request")
        self.assertEqual(response_data_dict["message"], "The 'to' and 'message' fields must not contain empty values.")
        delete_obj(self.token_obj)

    def test_send_sms_endpoint_when_no_to(self):
        """Tests the send sms endpoint when there is no to."""
        pay_load = {"me": ["+5018105654558"], "message": "hey there"}
        
        response = self.app.post('/v1/messages/sms', json=pay_load, headers=self.header)
        self.assertEqual(response.status_code, 400)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 400)
        self.assertEqual(response_data_dict["reason"], "Bad Request")
        self.assertEqual(response_data_dict["message"], "The 'to' and 'message' fields are required in the request body.")
        delete_obj(self.token_obj)

    def test_send_sms_endpoint_when_message_is_not_string(self):
        """Tests the send sms endpoint when message is not string."""
        pay_load = {"to": ["+5018105654558"], "message": ["hey there"]}
           
        response = self.app.post('/v1/messages/sms', json=pay_load, headers=self.header)
        self.assertEqual(response.status_code, 400)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 400)
        self.assertEqual(response_data_dict["reason"], "Bad Request")
        self.assertEqual(response_data_dict["message"], "The value of the 'message' field must be a string.")
        delete_obj(self.token_obj)

    def test_send_sms_endpoint_more_than_two_fields(self):
        """Tests the send sms endpoint when more than two keys in request json."""
        pay_load = {"to": ["+5018105654558"], "message": "hey there", "name": "Dennis"}
        
        response = self.app.post('/v1/messages/sms', json=pay_load, headers=self.header)
        self.assertEqual(response.status_code, 400)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 400)
        self.assertEqual(response_data_dict["reason"], "Bad Request")
        self.assertEqual(response_data_dict["message"], "You can't have more than two fields in the request json.")
        delete_obj(self.token_obj)

    def test_send_sms_endpoint_when_to_two_numbers_in_list(self):
        """Tests the send sms endpoint when to contains two phone number strings in list."""
        pay_load = {"to": ["2", "+5018105654558"], "message": "hey there"}
        
        response = self.app.post('/v1/messages/sms', json=pay_load, headers=self.header)
        self.assertEqual(response.status_code, 201)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        response_data_dict_item_length = len(response_data_dict["messages"])
        self.assertEqual(response_data_dict_item_length, 2)
        response_data_dict_item1_delivery_status = response_data_dict["messages"][0]["deliveryStatus"]
        self.assertEqual(response_data_dict_item1_delivery_status, "NotDelivered")
        response_data_dict_item2_delivery_status = response_data_dict["messages"][1]["deliveryStatus"]
        self.assertEqual(response_data_dict_item2_delivery_status, "DeliveredToNetwork")
        delete_obj(self.token_obj)

    def test_send_sms_endpoint_when_token_missing(self):
        """Test endpoint when token is omitted from the request."""
        
        pay_load = {"to": ["+5018105654558"], "message": "hey there"}
        
        response = self.app.post('/v1/messages/sms', json=pay_load)
        self.assertEqual(response.status_code, 401)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 401)
        self.assertEqual(response_data_dict["reason"], "Unauthorized")
        self.assertEqual(response_data_dict["message"], "Please provide an access token.")
        delete_obj(self.token_obj)
    
    def test_send_sms_endpoint_when_token_invalid(self):
        """Test endpoint for token that doesn't exist in the server."""
        token = {"access_token": '1700033395  .bad355fdfdc95d3b11cda8d6352ec5f7.VFJXfI  OBdqRC1xw8x08uZzvZgcxq2TMqgeh2icBT471=',  "expires_in": 1000}
        pay_load = {"to": ["+5018105654558"], "message": "hey there"}
        header = {'Authorization': token["access_token"]}

        response = self.app.post('/v1/messages/sms', json=pay_load, headers=header)
        self.assertEqual(response.status_code, 401)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 401)
        self.assertEqual(response_data_dict["reason"], "Unauthorized")
        self.assertEqual(response_data_dict["message"], "Please provide a valid access token.")
        delete_obj(self.token_obj)
    def test_send_sms_endpoint_when_token_expired(self):
    	delete_obj(self.token_obj)
     
    
def generate_token(expiry):
    """Generates and persists an access token."""
    token = {"access_token": '1700033395.bad355fdfdc95d3b11cda8d6352ec5f7.VFJXfIOBdqRC1xw8x08uZzvZgcxq2TMqgeh2icBT471=',"expires_in": expiry}
    new_token = AccessToken(**token)
    new_token.save()
    return new_token
