"""This module tests the end point for registering clients in the sms api.
"""

import unittest
import json
from v1.oauth.app import app
from v1.oauth.views.utils import delete_obj
from models.auth_code import AuthCode
from models.api_client import Client
from parameterized import parameterized

class ClientSecretTest(unittest.TestCase):
    """This tests the client secret endpoint."""
    def setUp(self):
        """Initializes external dependencies"""
        self.app = app.test_client()
        self.auth_code_obj = generate_auth_code()
        self.auth_code = self.auth_code_obj.code
        self.header = {'Authorization': self.auth_code}
    
    @parameterized.expand([
    	("no_auth", {"email": "dennisakpotaire@gmail.com"}, 401,  "Unauthorized", "Please provide an authorization code."),
    	("invalid_auth", {"email": "denniskoko@gmail.com"},  401,  "Unauthorized", "Please provide a valid authorization code."),
    ])
    def test_client_secret_endpoint_for_auth_code(self, case_name, pay_load, expected_code, expected_reason, expected_message):
        """Test endpoint for auth code associated edge cases."""
        response = None
        if case_name == "no_auth":
            response = self.app.post('/v1/oauth/client_secret', json=pay_load)
        elif case_name == "invalid_auth":
            auth_code = {"code": "746341", "client_email": "denniskoko@gmail.com", "expires_in": 2000}
            header = {'Authorization': auth_code["code"]}
       	    response = self.app.post('/v1/oauth/client_secret', headers=header, json=pay_load)
        self.assertEqual(response.status_code, expected_code)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], expected_code)
        self.assertEqual(response_data_dict["reason"], expected_reason)
        self.assertEqual(response_data_dict["message"], expected_message)
        delete_obj(self.auth_code_obj)
        
    #@unittest.skip("Couldn't get it implemnted yet.")
    #def test_client_secret_endpoint_when_auth_code_expired(self):
    	#pass
    
    
    @parameterized.expand([
    	({}, 400, "Bad Request", "The 'email' field is required in the request body."),
    	({"email": ""}, 400, "Bad Request", "The 'email' field must not contain an empty value."),
    	({"email": True}, 400, "Bad Request", "The value of the 'email' field must be a string."),
    	({"full_name": "Akpotaire Dennis", "email": "dennisakpotaire@gmail.com", "password": "12345", "sex": "male"}, 400, "Bad Request", "You can't have more than one field in the request json."),
    	({"email": "dennisakpotaire@gmail.com"}, 401, "Unauthorized", "You are not an existing client."),
    ])
    def test_client_secret_endpoint_for_email(self, pay_load, expected_code, expected_reason, expected_message):
        """Test endpoint for email associated edge cases."""
        
        response = self.app.post('/v1/oauth/client_secret', json=pay_load, headers=self.header)
        self.assertEqual(response.status_code, expected_code)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], expected_code)
        self.assertEqual(response_data_dict["reason"], expected_reason)
        self.assertEqual(response_data_dict["message"], expected_message)
        delete_obj(self.auth_code_obj)

    @parameterized.expand([
    	({"email": "dennisakpotaire@gmail.com"}, 201, 2),
    ])
    def test_client_secret_endpoint_correct_input(self, pay_load, expected_code, expected_length):
        """Test endpoint for correct input."""
        from models import storage 
        
        generate_client()
        response = self.app.post('/v1/oauth/client_secret', json=pay_load, headers=self.header)
        self.assertEqual(response.status_code, expected_code)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("client_id", response_data_dict)
        self.assertIn("new_client_secret", response_data_dict)
        response_data_dict_length = len(response_data_dict.keys())
        self.assertEqual(response_data_dict_length, expected_length)
        delete_obj(self.auth_code_obj)
        delete_obj(storage.get(Client, response_data_dict["client_id"]))
        

def generate_auth_code():
    """Generates and persists an authorization code."""
    auth_code = {"code": "746341", "client_email": "dennisakpotaire@gmail.com", "expires_in": 1000}
    new_code = AuthCode(**auth_code)
    new_code.save()
    return new_code

def generate_client():
    """Generates and persists a client."""
    client = {"full_name": "Akpotaire Dennis", "email": "dennisakpotaire@gmail.com", "password": "12345"}
    new_client = Client(**client)
    new_client.save()
