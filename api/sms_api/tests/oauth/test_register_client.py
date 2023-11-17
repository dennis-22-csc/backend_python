"""This module tests the end point for registering clients in the sms api.
"""

import unittest
import json
from v1.oauth.app import app
from v1.oauth.views.utils import delete_obj
from models.auth_code import AuthCode
from models.api_client import Client
from parameterized import parameterized

class RegisterClientTest(unittest.TestCase):
    """This tests the register client endpoint."""
    def setUp(self):
        """Initializes external dependencies"""
        self.app = app.test_client()
        self.auth_code_obj = generate_auth_code()
        self.auth_code = self.auth_code_obj.code
        self.header = {'Authorization': self.auth_code}
        
    @parameterized.expand([
      	("no_auth", {"full_name": "Akpotaire Dennis", "email": "dennisakpotaire@gmail.com", "password": "12345"}, 401, "Unauthorized", "Please provide an authorization code."),
        ("invalid_auth", {"full_name": "Dennis Koko", "email": "denniskoko@gmail.com", "password": "12345"}, 401, "Unauthorized", "Please provide a valid authorization code."),
    ])
    def test_register_client_endpoint_when_auth_code_invalid(self,  case_name, pay_load, expected_code, expected_reason, expected_message):
        """Test endpoint for auth code related edge cases."""
        response = None
        if case_name == "no_auth":
            response = self.app.post('/v1/oauth/register_client', json=pay_load)
        elif case_name == "invalid_auth":
            auth_code = {"code": "746341", "client_email": "denniskoko@gmail.com", "expires_in": 2000}
            header = {'Authorization': auth_code["code"]}
            response = self.app.post('/v1/oauth/register_client', headers=header, json=pay_load)
        self.assertEqual(response.status_code, expected_code)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], expected_code)
        self.assertEqual(response_data_dict["reason"], expected_reason)
        self.assertEqual(response_data_dict["message"], expected_message)
        delete_obj(self.auth_code_obj)
    
    @unittest.skip("Couldn't get it implemnted.")
    def test_register_client_endpoint_when_auth_code_expired(self):
    	pass
    
    @parameterized.expand([
        ({"email": "dennisakpotaire@gmail.com", "password": "12345"}, 400, "Bad Request", "The 'full_name', 'email', and 'password' fields are required in the request body."), # no full_name
        ({"full_name": "", "email": "dennisakpotaire@gmail.com", "password": "12345"}, 400, "Bad Request", "The 'full_name', 'email', and 'password' fields must not contain empty values."), # empty full_name
        ({"full_name": ["Akpotaire Dennis"], "email": "dennisakpotaire@gmail.com", "password": "12345"}, 400, "Bad Request", "The value of the 'full_name', 'email', and 'password' fields must be strings."), # full_name not string
        ({"full_name": "Akpotaire Dennis", "password": "12345"}, 400, "Bad Request", "The 'full_name', 'email', and 'password' fields are required in the request body."), # no email
    	({"full_name": "Akpotaire Dennis","email": "", "password": "12345"}, 400, "Bad Request", "The 'full_name', 'email', and 'password' fields must not contain empty values."), # empty email
    	({"full_name": "Akpotaire Dennis","email": True, "password": "12345"}, 400, "Bad Request", "The value of the 'full_name', 'email', and 'password' fields must be strings."), # email is not string
    	({"full_name": "Akpotaire Dennis", "email": "dennisakpotaire@gmail.com"}, 400, "Bad Request", "The 'full_name', 'email', and 'password' fields are required in the request body."),# no password
    	({"full_name": "Akpotaire Dennis","email": "dennisakpotaire@gmail.com", "password": ""}, 400, "Bad Request", "The 'full_name', 'email', and 'password' fields must not contain empty values."), # empty password
    	({"full_name": "Akpotaire Dennis", "email": "dennisakpotaire@gmail.com", "password": 12345}, 400, "Bad Request",  "The value of the 'full_name', 'email', and 'password' fields must be strings."), # password is not string
    	({"full_name": "Akpotaire Dennis", "email": "dennisakpotaire@gmail.com", "password": "12345", "sex": "male"}, 400, "Bad Request", "You can't have more than three fields in the request json.") # more than three fields in request body
    ])
    def test_register_client_endpoint_for_full_name_email_password_edge_cases(self, pay_load, expected_code, expected_reason, expected_message):
        """Test the register_client_endpoint for full_name, email and password associated edge cases."""
        
        response = self.app.post('/v1/oauth/register_client', json=pay_load, headers=self.header)
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
    	({"full_name": "Akpotaire Dennis", "email": "dennisakpotaire@gmail.com", "password": "12345"}, 201, 3), 
    ])
    def test_register_client_endpoint_correct_input(self, pay_load, expected_code, expected_length):
        """Test endpoint for correct input."""
        from models import storage 
        
        response = self.app.post('/v1/oauth/register_client', json=pay_load, headers=self.header)
        self.assertEqual(response.status_code, expected_code)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("status", response_data_dict)
        self.assertIn("client_id", response_data_dict)
        self.assertIn("client_secret", response_data_dict)
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

