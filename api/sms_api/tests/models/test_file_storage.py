"""This module tests the file_storage module.
"""

import unittest
import json
from datetime import datetime, timedelta
from models import storage
from models.access_token import AccessToken
from parameterized import parameterized

class FileStorageTest(unittest.TestCase):
    """This tests the FileStorage class."""
    def setUp(self):
        """Initializes external dependencies"""
        pass
      
    @parameterized.expand([
      	("obj1", {"access_token": "rrr", "expires_in": 1000}),
      	("obj2", {"access_token": "ppp", "expires_in": 1000}),
      	("obj3", {"access_token": "qqqr", "expires_in": 1000})
    ])   
    def test_all(self, name, token_dict):
        """Tests the storage.all function."""
        
        new_token = AccessToken(**token_dict)
        
        tokens = storage.all(AccessToken)
        self.assertEqual(True, any(new_token.to_dict() == token.to_dict() for token in tokens.values()))
        for token in tokens.values():
            current_token = token
            self.assertEqual(datetime, type(current_token.created_at))
            current_token = token.to_dict()
            self.assertEqual(str, type(current_token["created_at"]))
