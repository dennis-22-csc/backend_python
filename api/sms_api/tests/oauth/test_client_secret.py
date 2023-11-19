"""This module tests the end point for registering clients in the sms api.

"""

import unittest
import json
from v1.oauth.app import app
from models.auth_code import AuthCode
from parameterized import parameterized
from unittest.mock import patch, Mock, MagicMock
from v1.oauth.views.auth_server import AuthServer

class ClientSecretTest(unittest.TestCase):
    """This tests the client secret endpoint."""
    def setUp(self):
        """Initializes external dependencies"""
        self.app = app.test_client()
        self.auth_code = "746341" 
        self.header = {'Authorization': self.auth_code}
    
    @parameterized.expand([
    	("no_auth", {"email": "dennisakpotaire@gmail.com"}, 401,  "Unauthorized", "Please provide an authorization code."),
    	("invalid_auth", {"email": "denniskoko@gmail.com"},  401,  "Unauthorized", "Please provide a valid authorization code."),
    ("expired_auth", {"email": "ayodeleoluwaseun@gmail.com"}, 401, "Unauthorized", "Authorization code has expired."),
    ])
    @patch('v1.oauth.views.index.delete_obj')
    @patch('v1.oauth.views.index.has_expired')
    @patch('v1.oauth.views.index.validate_auth_code')
    def test_client_secret_endpoint_for_auth_code(self, case_name, pay_load, expected_code, expected_reason, expected_message, mock_validate_auth_code, mock_has_expired, mock_delete_obj):
        """Test endpoint for auth code associated edge cases."""
        response = None
        if case_name == "no_auth":
            response = self.app.post('/v1/oauth/client_secret', json=pay_load)
            mock_validate_auth_code.assert_not_called()
        elif case_name == "invalid_auth":
            mock_validate_auth_code.return_value = None
            response = self.app.post('/v1/oauth/client_secret', headers=self.header, json=pay_load)
            mock_validate_auth_code.assert_called_once()
            mock_validate_auth_code.assert_called_once_with(self.auth_code, pay_load["email"])
        elif case_name == "expired_auth":
            auth_obj_mock = Mock(spec=AuthCode)
            mock_validate_auth_code.return_value = auth_obj_mock
            mock_has_expired.return_value = True
            response = self.app.post('/v1/oauth/client_secret', headers=self.header, json=pay_load)
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
    	({}, 400, "Bad Request", "The 'email' field is required in the request body."),
    	({"email": ""}, 400, "Bad Request", "The 'email' field must not contain an empty value."),
    	({"email": True}, 400, "Bad Request", "The value of the 'email' field must be a string."),
    	({"full_name": "Akpotaire Dennis", "email": "dennisakpotaire@gmail.com", "password": "12345", "sex": "male"}, 400, "Bad Request", "You can't have more than one field in the request json."),
    	({"email": "dennisakpotaire@gmail.com"}, 401, "Unauthorized", "You are not an existing client."),
    ])
    @patch('v1.oauth.views.index.client_exist')
    @patch('v1.oauth.views.index.has_expired')
    @patch('v1.oauth.views.index.validate_auth_code')
    def test_client_secret_endpoint_for_email(self, pay_load, expected_code, expected_reason, expected_message,mock_validate_auth_code,mock_has_expired, mock_client_exist):
        """Test endpoint for email associated edge cases."""
        auth_obj_mock = Mock(spec=AuthCode)
        mock_validate_auth_code.return_value = auth_obj_mock
        mock_has_expired.return_value = False
        mock_client_exist.return_value = False
        response = self.app.post('/v1/oauth/client_secret', json=pay_load, headers=self.header)
        self.assertEqual(response.status_code, expected_code)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("code", response_data_dict)
        self.assertIn("reason", response_data_dict)
        self.assertIn("message", response_data_dict)
        self.assertEqual(response_data_dict["code"], expected_code)
        self.assertEqual(response_data_dict["reason"], expected_reason)
        self.assertEqual(response_data_dict["message"], expected_message)
        
  
  
    @parameterized.expand([
    	({"email": "dennisakpotaire@gmail.com"}, 201, 2), 
    ])
    @patch('v1.oauth.views.auth_server.update_obj')
    @patch.object(AuthServer,'generate_client_secret',autospec=True)
    @patch('v1.oauth.views.index.client_exist')
    @patch('v1.oauth.views.index.has_expired')
    @patch('v1.oauth.views.index.validate_auth_code')
    def test_client_secret_endpoint_correct_input(self, pay_load, expected_code, expected_length, mock_validate_auth_code, mock_has_expired, mock_client_exist, mock_generate_client_secret,mock_update_obj):
        """Test endpoint for correct input."""
        auth_obj_mock = Mock(spec=AuthCode)
        mock_validate_auth_code.return_value = auth_obj_mock
        mock_has_expired.return_value = False
        mock_client_exist.return_value = True 
        mock_generate_client_secret.return_value = "yyyyeeeeffff"
        mock_update_obj.return_value = MagicMock(id=1, secret='yyyyeeeeffff')
        response = self.app.post('/v1/oauth/client_secret', json=pay_load, headers=self.header) 
        self.assertEqual(response.status_code, expected_code)
        response_data_dict = json.loads(response.data.decode('utf-8'))
        self.assertIn("client_id", response_data_dict)
        self.assertIn("new_client_secret", response_data_dict)
        response_data_dict_length = len(response_data_dict.keys())
        self.assertEqual(response_data_dict_length, expected_length)
  
    
