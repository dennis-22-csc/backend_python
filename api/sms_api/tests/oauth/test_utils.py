"""This module tests the functions in the utils module.
"""

import unittest
from models.access_token import AccessToken
from models.auth_code import AuthCode
from models.base_model import BaseModel
from unittest.mock import Mock, patch, MagicMock
from v1.oauth.views.utils import has_expired, delete_obj, validate_token, save_obj, update_obj, email_client, validate_auth_code, client_exist, get_client_ids, get_client_secrets
from parameterized import parameterized
from models.api_client import Client
from v1.oauth.views.gmail_smtp import GmailSMTPService
from v1.oauth.views.email_service import EmailService

class UtilsTest(unittest.TestCase):
    """This tests the functions in the utils module."""
    def setUp(self):
        """Initializes external dependencies"""
        pass
    
    @parameterized.expand([       (AccessToken(access_token="dfwqast", expires_in=900), False),
        (BaseModel(), ValueError),
        (Mock(), ValueError),
    ])
    def test_has_expired(self, input_data, expected_result):
        if expected_result == ValueError:
            self.assertRaises(ValueError, has_expired, input_data)
        else:
            result = has_expired(input_data)
            self.assertEqual(expected_result, result)
  
  
    @parameterized.expand([      (AccessToken(access_token="dfwqast", expires_in=900), True),
        (Mock(), ValueError),
    ])
    @patch('models.storage.save')
    @patch('models.storage.delete')
    def test_delete_obj(self, my_obj, expected_result, mock_delete, mock_save):
        mock_delete.return_value = True
        mock_save.return_value = True
        if expected_result == ValueError:
            self.assertRaises(ValueError, delete_obj, my_obj)
        else:
            result = delete_obj(my_obj)
            self.assertEqual(expected_result, result)
            mock_delete.assert_called_once()
            mock_delete.assert_called_once_with(my_obj)
            mock_save.assert_called_once()

    @parameterized.expand([      
        ("dfwqast", AccessToken(access_token="dfwqast", expires_in=900)),
        ("dfwqasa", None)
    ])
    @patch('models.storage.all')
    def test_validate_token(self, my_token, expected_result, mock_all):
        mock_all.return_value = {"1": AccessToken(access_token="dfwqast", expires_in=900), "2": AccessToken(access_token="qfwqast", expires_in=900), "3": AccessToken(access_token="afwqast", expires_in=900), "4": AccessToken(access_token="zfwqast", expires_in=900), "5": AccessToken(access_token="yfwqast", expires_in=900)}
        result = validate_token(my_token)
        if result:
            self.assertEqual(result.access_token, expected_result.access_token)
        else:
            self.assertEqual(result, expected_result)

    @parameterized.expand([
        (AccessToken, {"access_token":"dfwqast", "expires_in": 900}, AccessToken(access_token="dfwqast", expires_in=900)),
        (Mock, {"access_token": "outfds", "expires_in": 700}, ValueError),
    ])
    @patch.object(BaseModel, 'save', autospec=True)
    def test_save_obj(self, my_class, my_dict, expected_result, mock_save):
        mock_save.return_value = True
        if expected_result == ValueError:
            self.assertRaises(ValueError, save_obj, my_class, my_dict)
        else:
            result = save_obj(my_class, my_dict)
            self.assertEqual(expected_result.access_token, result.access_token)
            mock_save.assert_called_once()

    @parameterized.expand([
        (Client, {"full_name": "Dennis Koko", "password": "54321"}, "denniskoko@gmail.com", None),
        (Client, {"full_name": "Alimat Abimbola", "password": "700"}, "abimbolaalimat@gmail.com", Client(full_name="Alimat Abimbola", password="700")), 
        (Mock, {"full_name": "Alimat Abimbola", "password": "700"}, "abimbolaalimat@gmail.com", ValueError),
    ])
    @patch.object(BaseModel, 'save', autospec=True)
    @patch('models.storage.all')
    def test_update_obj(self, class_name, info_dict, email, expected_result, mock_all, mock_save):
        mock_all.return_value = {"1": Client(full_name="Dennis Babs", password="900", email="dennisko@gmail.com"), "2": Client(full_name="Alimat Goks", password="9001", email="abimbolaalimat@gmail.com")} 
        
        mock_save.return_value = True
        if expected_result == ValueError:
            self.assertRaises(ValueError, update_obj, class_name, info_dict, email)
        else:
            result = update_obj(class_name, info_dict, email)
            if result:
                self.assertEqual(expected_result.full_name, result.full_name)
                self.assertEqual(expected_result.password, result.password)
                mock_save.assert_called_once()
            else:
                self.assertEqual(expected_result, result)

    @parameterized.expand([
        ("denniskoko@gmail.com", "Authorization", "Hey Dennis! Welcome"), 
    ])
    @patch.object(GmailSMTPService, 'send_email', autospec=True)
    @patch.object(EmailService, 'create_email_service', autospec=True)
    def test_email_client(self, client_address, subject, body, mock_create_email_service, mock_send_email):
        mock_create_email_service.return_value = Mock(spec=GmailSMTPService)
        mock_send_email.return_value = True
        result = email_client(client_address, subject, body)
        self.assertEqual(True, result)


    @parameterized.expand([      
        ("dfwqast", "denniskoko@gmail.com", AuthCode(code="dfwqast", client_email="denniskoko@gmail.com", expires_in=900)),
        ("dfwqasa", "abimbolaalimat@gmail.com", None)
    ])
    @patch('models.storage.all')
    def test_validate_auth_code(self, my_code, email, expected_result, mock_all):
        mock_all.return_value = {"1": AuthCode(code="dfwqast", client_email="denniskoko@gmail.com", expires_in=900), "2": AuthCode(code="qfwqast", client_email="abimbolaalimat13@gmail.com", expires_in=900), "3": AuthCode(code="afwqast", client_email="johndoe@gmail.com",expires_in=900), "4": AuthCode(code="zfwqast", client_email="budescode@gmail.com",expires_in=900), "5": AuthCode(code="yfwqast", client_email="yammy@gmail.com",expires_in=900)}
        result = validate_auth_code(my_code, email)
        if result:
            self.assertEqual(result.code, expected_result.code)
        else:
            self.assertEqual(result, expected_result)

    @parameterized.expand([
    ("denniskoko@gmail.com", True),
    ("abimbolaalimat@gmail.com", False),
    ])
    @patch('models.storage.all')
    def test_client_exist(self, email, expected_result, mock_all):
        mock_all.return_value = {"1": Client(full_name="Dennis Babs", password="900", email="denniskoko@gmail.com"), "2": Client(full_name="Alimat Goks", password="9001", email="abimbolaalimat13@gmail.com")}
        result = client_exist(email)
        
        self.assertEqual(expected_result, result)

    @patch('models.storage.all')
    def test_get_client_ids(self, mock_all):
        mock_all.return_value = {"1": Client(id=1, full_name="Dennis Babs", password="900", email="denniskoko@gmail.com", secret="swagqueds"), "2": Client(id=2, full_name="Alimat Goks", password="9001", email="abimbolaalimat13@gmail.com", secret="pqurgx")}
        result = get_client_ids()
        self.assertEqual(len(result), 2)
        self.assertIn(2, result)
        self.assertIn(1, result)
        self.assertNotIn(3, result) 


    @patch('models.storage.all')
    def test_get_client_secrets(self, mock_all):
        mock_all.return_value = {"1": Client(full_name="Dennis Babs", password="900", email="denniskoko@gmail.com", secret="swagqueds"), "2": Client(full_name="Alimat Goks", password="9001", email="abimbolaalimat13@gmail.com", secret="pqurgx")}
        result = get_client_secrets()
        self.assertEqual(len(result), 2)
        self.assertIn("swagqueds", result)
        self.assertIn("pqurgx", result)
        self.assertNotIn("swwpihd", result) 
