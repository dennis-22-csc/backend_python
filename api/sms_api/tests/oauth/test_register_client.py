"""This module tests the end point for registering clients in the sms api.
"""

import unittest
import json
from v1.oauth.app import app
from v1.oauth.views.utils import delete_obj
from models.auth_code import AuthCode
from models.api_client import Client

class RegisterClientTest(unittest.TestCase):
    """This tests the register client endpoint."""
    def setUp(self):
        """Initializes external dependencies"""
        self.app = app.test_client()
        self.auth_code_obj = generate_auth_code()
        self.auth_code = self.auth_code_obj.code
        self.header = {'Authorization': self.auth_code}
        
    def test_register_client_endpoint_when_auth_code_missing(self):
        """Test endpoint when auth code is omitted from the request."""
        
        pay_load = {"full_name": "Akpotaire Dennis", "email": "dennisakpotaire@gmail.com", "password": "12345"}
        
        response = self.app.post('/v1/oauth/register_client', json=pay_load)
        self.assertEqual(response.status_code, 401)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 401)
        self.assertEqual(response_data_dict["reason"], "Unauthorized")
        self.assertEqual(response_data_dict["message"], "Please provide an authorization code.")
        delete_obj(self.auth_code_obj)
        
    def test_register_client_endpoint_when_auth_code_invalid(self):
        """Test endpoint for auth code that doesn't exist in the server."""
        auth_code = {"code": "746341", "client_email": "denniskoko@gmail.com", "expires_in": 2000}
        header = {'Authorization': auth_code["code"]}

        pay_load = {"full_name": "Dennis Koko", "email": "denniskoko@gmail.com", "password": "12345"}
        
        response = self.app.post('/v1/oauth/register_client', headers=header, json=pay_load)
        self.assertEqual(response.status_code, 401)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 401)
        self.assertEqual(response_data_dict["reason"], "Unauthorized")
        self.assertEqual(response_data_dict["message"], "Please provide a valid authorization code.")
        delete_obj(self.auth_code_obj)
    
    @unittest.skip("Couldn't get it implemnted.")
    def test_register_client_endpoint_when_auth_code_expired(self):
    	pass
    
    def test_register_client_endpoint_when_full_name_missing(self):
        """Test endpoint when full name is omitted from the request."""
        
        pay_load = {"email": "dennisakpotaire@gmail.com", "password": "12345"}
        
        response = self.app.post('/v1/oauth/register_client', json=pay_load, headers=self.header)
        self.assertEqual(response.status_code, 400)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 400)
        self.assertEqual(response_data_dict["reason"], "Bad Request")
        self.assertEqual(response_data_dict["message"], "The 'full_name', 'email', and 'password' fields are required in the request body.")
        delete_obj(self.auth_code_obj)

    def test_register_client_endpoint_when_full_name_empty_string(self):
        """Test endpoint when full name is an empty string."""
        
        pay_load = {"full_name": "","email": "dennisakpotaire@gmail.com", "password": "12345"}
        
        response = self.app.post('/v1/oauth/register_client', json=pay_load, headers=self.header)
        self.assertEqual(response.status_code, 400)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 400)
        self.assertEqual(response_data_dict["reason"], "Bad Request")
        self.assertEqual(response_data_dict["message"],  "The 'full_name', 'email', and 'password' fields must not contain empty values.")
        delete_obj(self.auth_code_obj)

    def test_register_client_endpoint_when_full_name_is_no_string(self):
        """Test endpoint when full name is no string."""
        
        pay_load = {"full_name": ["Akpotaire Dennis"],"email": "dennisakpotaire@gmail.com", "password": "12345"}
        
        response = self.app.post('/v1/oauth/register_client', json=pay_load, headers=self.header)
        self.assertEqual(response.status_code, 400)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 400)
        self.assertEqual(response_data_dict["reason"], "Bad Request")
        self.assertEqual(response_data_dict["message"],  "The value of the 'full_name', 'email', and 'password' fields must be strings.")
        delete_obj(self.auth_code_obj)
        
    def test_register_client_endpoint_when_email_missing(self):
        """Test endpoint when email is omitted from the request."""
        
        pay_load = {"full_name": "Akpotaire Dennis", "password": "12345"}
        
        response = self.app.post('/v1/oauth/register_client', json=pay_load, headers=self.header)
        self.assertEqual(response.status_code, 400)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 400)
        self.assertEqual(response_data_dict["reason"], "Bad Request")
        self.assertEqual(response_data_dict["message"], "The 'full_name', 'email', and 'password' fields are required in the request body.")
        delete_obj(self.auth_code_obj)

    def test_register_client_endpoint_when_email_empty_string(self):
        """Test endpoint when email is an empty string."""
        
        pay_load = {"full_name": "Akpotaire Dennis","email": "", "password": "12345"}
        
        response = self.app.post('/v1/oauth/register_client', json=pay_load, headers=self.header)
        self.assertEqual(response.status_code, 400)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 400)
        self.assertEqual(response_data_dict["reason"], "Bad Request")
        self.assertEqual(response_data_dict["message"],  "The 'full_name', 'email', and 'password' fields must not contain empty values.")
        delete_obj(self.auth_code_obj)

    def test_register_client_endpoint_when_email_is_no_string(self):
        """Test endpoint when email is no string."""
        
        pay_load = {"full_name": "Akpotaire Dennis","email": True, "password": "12345"}
        
        response = self.app.post('/v1/oauth/register_client', json=pay_load, headers=self.header)
        self.assertEqual(response.status_code, 400)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 400)
        self.assertEqual(response_data_dict["reason"], "Bad Request")
        self.assertEqual(response_data_dict["message"],  "The value of the 'full_name', 'email', and 'password' fields must be strings.")
        delete_obj(self.auth_code_obj)
        
    def test_register_client_endpoint_when_password_missing(self):
        """Test endpoint when password is omitted from the request."""
        
        pay_load = {"full_name": "Akpotaire Dennis", "email": "dennisakpotaire@gmail.com"}
        
        response = self.app.post('/v1/oauth/register_client', json=pay_load, headers=self.header)
        self.assertEqual(response.status_code, 400)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 400)
        self.assertEqual(response_data_dict["reason"], "Bad Request")
        self.assertEqual(response_data_dict["message"], "The 'full_name', 'email', and 'password' fields are required in the request body.")
        delete_obj(self.auth_code_obj)

    def test_register_client_endpoint_when_password_empty_string(self):
        """Test endpoint when password is an empty string."""
        
        pay_load = {"full_name": "Akpotaire Dennis","email": "dennisakpotaire@gmail.com", "password": ""}
        
        response = self.app.post('/v1/oauth/register_client', json=pay_load, headers=self.header)
        self.assertEqual(response.status_code, 400)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 400)
        self.assertEqual(response_data_dict["reason"], "Bad Request")
        self.assertEqual(response_data_dict["message"],  "The 'full_name', 'email', and 'password' fields must not contain empty values.")
        delete_obj(self.auth_code_obj)

    def test_register_client_endpoint_when_password_is_no_string(self):
        """Test endpoint when password is an no string."""
        
        pay_load = {"full_name": "Akpotaire Dennis", "email": "dennisakpotaire@gmail.com", "password": 12345}
        
        response = self.app.post('/v1/oauth/register_client', json=pay_load, headers=self.header)
        self.assertEqual(response.status_code, 400)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 400)
        self.assertEqual(response_data_dict["reason"], "Bad Request")
        self.assertEqual(response_data_dict["message"],  "The value of the 'full_name', 'email', and 'password' fields must be strings.")
        delete_obj(self.auth_code_obj)
        
    def test_register_client_endpoint_more_than_three_fields(self):
        """Test endpoint for more than three fields."""
        
        pay_load = {"full_name": "Akpotaire Dennis", "email": "dennisakpotaire@gmail.com", "password": "12345", "sex": "male"}
        
        response = self.app.post('/v1/oauth/register_client', json=pay_load, headers=self.header)
        self.assertEqual(response.status_code, 400)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], 400)
        self.assertEqual(response_data_dict["reason"], "Bad Request")
        self.assertEqual(response_data_dict["message"], "You can't have more than three fields in the request json.")
        delete_obj(self.auth_code_obj)
        
    def test_register_client_endpoint_correct_input(self):
        """Test endpoint for correct input."""
        from models import storage 
        
        pay_load = {"full_name": "Akpotaire Dennis", "email": "dennisakpotaire@gmail.com", "password": "12345"}
        
        response = self.app.post('/v1/oauth/register_client', json=pay_load, headers=self.header)
        self.assertEqual(response.status_code, 201)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("status", response_data_dict)
        self.assertIn("client_id", response_data_dict)
        self.assertIn("client_secret", response_data_dict)
        response_data_dict_length = len(response_data_dict.keys())
        self.assertEqual(response_data_dict_length, 3)
        delete_obj(self.auth_code_obj)
        delete_obj(storage.get(Client, response_data_dict["client_id"]))
        

def generate_auth_code():
    """Generates and persists an authorization code."""
    auth_code = {"code": "746341", "client_email": "dennisakpotaire@gmail.com", "expires_in": 1000}
    new_code = AuthCode(**auth_code)
    new_code.save()
    return new_code

