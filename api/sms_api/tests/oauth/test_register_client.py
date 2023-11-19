"""This module tests the end point for registering clients in the sms api.
"""

import unittest
import json
from v1.oauth.app import app
from models.auth_code import AuthCode
from parameterized import parameterized
from unittest.mock import patch, Mock, MagicMock
from models.auth_code import AuthCode
from v1.oauth.views.auth_server import AuthServer


class RegisterClientTest(unittest.TestCase):
    """This tests the register client endpoint."""
    def setUp(self):
        """Initializes external dependencies"""
        self.app = app.test_client()
        self.auth_code = "746341" 
        self.header = {'Authorization': self.auth_code}
        
    @parameterized.expand([
      	("no_auth", {"full_name": "Akpotaire Dennis", "email": "dennisakpotaire@gmail.com", "password": "12345"}, 401, "Unauthorized", "Please provide an authorization code."),
        ("invalid_auth", {"full_name": "Dennis Koko", "email": "denniskoko@gmail.com", "password": "12345"}, 401, "Unauthorized", "Please provide a valid authorization code."),
        ("expired_auth", {"full_name": "Ayodele Oluwaseun", "email": "ayodeleoluwaseun@gmail.com", "password": "12345"}, 401, "Unauthorized", "Authorization code has expired."),
    ])
    @patch('v1.oauth.views.index.delete_obj')
    @patch('v1.oauth.views.index.has_expired')
    @patch('v1.oauth.views.index.validate_auth_code')
    def test_register_client_endpoint_when_auth_code_invalid(self,  case_name, pay_load, expected_code, expected_reason, expected_message, mock_validate_auth_code, mock_has_expired, mock_delete_obj):
        """Test endpoint for auth code related edge cases."""
        response = None
        if case_name == "no_auth":
            response = self.app.post('/v1/oauth/register_client', json=pay_load)
            mock_validate_auth_code.assert_not_called()
        elif case_name == "invalid_auth":
            mock_validate_auth_code.return_value = None
            response = self.app.post('/v1/oauth/register_client', headers=self.header, json=pay_load)
            mock_validate_auth_code.assert_called_once()
            mock_validate_auth_code.assert_called_once_with(self.auth_code, pay_load["email"])
        elif case_name == "expired_auth":
            auth_obj_mock = Mock(spec=AuthCode)
            mock_validate_auth_code.return_value = auth_obj_mock
            mock_has_expired.return_value = True
            response = self.app.post('/v1/oauth/register_client', headers=self.header, json=pay_load)
            mock_validate_auth_code.assert_called_once()
            mock_validate_auth_code.assert_called_once_with(self.auth_code, pay_load["email"])
            mock_has_expired.assert_called_once()
            mock_has_expired.assert_called_once_with(auth_obj_mock)
        
        self.assertEqual(response.status_code, expected_code)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], expected_code)
        self.assertEqual(response_data_dict["reason"], expected_reason)
        self.assertEqual(response_data_dict["message"], expected_message)
    
    
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
    
    @parameterized.expand([
    	("new_client", {"full_name": "Akpotaire Dennis", "email": "dennisakpotaire@gmail.com", "password": "12345"}, 201, 3, "", ""),
    ("existing_client", {"full_name": "Ayodele Oluwaseun", "email": "ayodeleoluwaseun@gmail.com", "password": "12345"}, 500, 3, "Internal Server Error", "Email address already exists."), 
    ("not_saved_client", {"full_name": "Alimat Sadiat", "email": "alimatsadiat@gmail.com", "password": "12345"}, 500, 3, "Internal Server Error", "An error occurred in the process of registering your info."), 
    ])
    @patch('v1.oauth.views.auth_server.save_obj')
    @patch.object(AuthServer,'generate_client_secret',autospec=True)
    @patch('v1.oauth.views.auth_server.hash_password')
    @patch('v1.oauth.views.auth_server.client_exist')
    @patch('v1.oauth.views.index.has_expired')
    @patch('v1.oauth.views.index.validate_auth_code')
    def test_register_client_endpoint_correct_input(self, case_name, pay_load, expected_code, expected_length, expected_reason, expected_message,  mock_validate_auth_code, mock_has_expired, mock_client_exist, mock_hash_password, mock_generate_client_secret, mock_save_obj):
        """Test endpoint for correct input."""
        auth_obj_mock = Mock(spec=AuthCode)
        mock_validate_auth_code.return_value = auth_obj_mock
        mock_has_expired.return_value = False
        if case_name == "new_client":
            mock_client_exist.return_value = False
            mock_hash_password.decode.return_value = "xxxxxhhhhhooooo"
            mock_generate_client_secret.return_value = "yyyyeeeeffff"
            mock_save_obj.return_value = MagicMock(id=1, secret='yyyyeeeeffff')
            response = self.app.post('/v1/oauth/register_client', json=pay_load, headers=self.header)
            self.assertEqual(response.status_code, expected_code)
            response_data_dict = json.loads(response.data.decode('utf-8'))
            self.assertIn("status", response_data_dict)
            self.assertIn("client_id", response_data_dict)
            self.assertIn("client_secret", response_data_dict)
            response_data_dict_length = len(response_data_dict.keys())
            self.assertEqual(response_data_dict_length, expected_length)
        elif case_name == "existing_client":
            mock_client_exist.return_value = True
            response = self.app.post('/v1/oauth/register_client', json=pay_load, headers=self.header)
            self.assertEqual(response.status_code, expected_code)
            response_data_dict = json.loads(response.data.decode('utf-8'))
            self.assertIn("code", response_data_dict)
            self.assertIn("reason", response_data_dict)
            self.assertIn("message", response_data_dict)
            self.assertEqual(response_data_dict["code"], expected_code)
            self.assertEqual(response_data_dict["reason"], expected_reason)
            self.assertEqual(response_data_dict["message"], expected_message)
        elif case_name == "not_saved_client":
            mock_client_exist.return_value = False
            mock_hash_password.decode.return_value = "xxxxxhhhhhooooo"
            mock_generate_client_secret.return_value = "yyyyeeeeffff"
            mock_save_obj.return_value = None
            response = self.app.post('/v1/oauth/register_client', json=pay_load, headers=self.header)
            self.assertEqual(response.status_code, expected_code)
            response_data_dict = json.loads(response.data.decode('utf-8'))
            self.assertIn("code", response_data_dict)
            self.assertIn("reason", response_data_dict)
            self.assertIn("message", response_data_dict)
            self.assertEqual(response_data_dict["code"], expected_code)
            self.assertEqual(response_data_dict["reason"], expected_reason)
            self.assertEqual(response_data_dict["message"], expected_message)
