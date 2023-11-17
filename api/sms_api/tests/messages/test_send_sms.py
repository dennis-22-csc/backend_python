"""This module tests the end point for sending sms in the sms api.
"""

import unittest
import json
from v1.messages.app import app
from v1.oauth.views.utils import delete_obj
from models.access_token import AccessToken
from parameterized import parameterized

class SendSmsTest(unittest.TestCase):
    """This tests the send sms endpoint."""
    def setUp(self):
        """Initializes external dependencies"""
        self.app = app.test_client()
        self.token_obj = generate_token(1000)
        self.token = self.token_obj.access_token
        self.header = {'Authorization': self.token}
    
    @parameterized.expand([
    	({"to": ["2"], "message": "hey there"}, 201, 1, ["NotDelivered"]),
    	({"to": ["+5018105654558"], "message": "hey there"}, 201, 1, ["DeliveredToNetwork"]),
    	({"to": ["2", "+5018105654558"], "message": "hey there"}, 201, 2, ["NotDelivered", "DeliveredToNetwork"]),
    ])
    def test_send_sms_endpoint_phone_numbers(self, pay_load, expected_code, expected_length, expected_delivery_status):
        """Tests the send sms endpoint when to doesn't contain a valid e164 phone number."""
        
        response = self.app.post('/v1/messages/sms', json=pay_load, 
headers=self.header)
        self.assertEqual(response.status_code, expected_code)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        response_data_dict_item_length = len(response_data_dict["messages"])
        self.assertEqual(response_data_dict_item_length, expected_length)
        for i in range(len(response_data_dict["messages"])):
        	response_data_dict_item_delivery_status = response_data_dict["messages"][i]["deliveryStatus"]
        	self.assertEqual(response_data_dict_item_delivery_status, expected_delivery_status[i])
        delete_obj(self.token_obj)
     
    @parameterized.expand([
    	({"to": [[2]], "message": "hey there"}, 400,  "Bad Request",  "The value of the 'to' field must be a list containing at least one string of phone numbers.", ),
    	({"to": 5018105654558, "message": "hey there"},  400,  "Bad Request", "The value of the 'to' field must be a list containing at least one phone number."),
    	({"to": [""], "message": "hey there"},  400,  "Bad Request", "The value of the 'to' field must be a list containing at least one phone number."),
    	({"to": [], "message": "hey there"}, 400,  "Bad Request", "The 'to' and 'message' fields must not contain empty values.", ),
    	({"me": ["+5018105654558"], "message": "hey there"}, 400,  "Bad Request", "The 'to' and 'message' fields are required in the request body."),
    	({"to": ["+5018105654558"], "message": ["hey there"]},  400,  "Bad Request", "The value of the 'message' field must be a string."),
    	({"to": ["+5018105654558"], "message": "hey there", "name": "Dennis"}, 400,  "Bad Request", "You can't have more than two fields in the request json."),
    ])
    def test_send_sms_endpoint_bad_requests(self, pay_load, expected_code, expected_reason, expected_message):
        """Tests endpoint for bad requests."""
          
        response = self.app.post('/v1/messages/sms', json=pay_load, headers=self.header)
        self.assertEqual(response.status_code, expected_code)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], expected_code)
        self.assertEqual(response_data_dict["reason"], expected_reason)
        self.assertEqual(response_data_dict["message"], expected_message)
        delete_obj(self.token_obj)

    @parameterized.expand([
    	("no_token", {"to": ["+5018105654558"], "message": "hey there"}, 401, "Unauthorized", "Please provide an access token."),
    	("invalid_token", {"to": ["+5018105654558"], "message": "hey there"}, 401, "Unauthorized", "Please provide a valid access token."),
    ])
    def test_send_sms_endpoint_token(self, case_name, pay_load, expected_code, expected_reason, expected_message):
        """Test endpoint for token associated edge cases"""
        response = None
        if case_name == "no_token":
            response = self.app.post('/v1/messages/sms', json=pay_load)
        elif case_name == "invalid_token":
            token = {"access_token": '1700033395  .bad355fdfdc95d3b11cda8d6352ec5f7.VFJXfI  OBdqRC1xw8x08uZzvZgcxq2TMqgeh2icBT471=',  "expires_in": 1000}
            header = {'Authorization': token["access_token"]}
            response = self.app.post('/v1/messages/sms', json=pay_load, headers=header)
        self.assertEqual(response.status_code, expected_code)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], expected_code)
        self.assertEqual(response_data_dict["reason"], expected_reason)
        self.assertEqual(response_data_dict["message"], expected_message)
        delete_obj(self.token_obj)
    
    #@unittest.skip("Couldn't get it implemnted yet.")
    #def test_send_sms_endpoint_when_token_expired(self):
    	#pass
     
    
def generate_token(expiry):
    """Generates and persists an access token."""
    token = {"access_token": '1700033395.bad355fdfdc95d3b11cda8d6352ec5f7.VFJXfIOBdqRC1xw8x08uZzvZgcxq2TMqgeh2icBT471=',"expires_in": expiry}
    new_token = AccessToken(**token)
    new_token.save()
    return new_token
