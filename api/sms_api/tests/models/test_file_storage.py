"""This module tests the file_storage module.
"""

import unittest
import json
from datetime import datetime, timedelta
from models import storage
from models.access_token import AccessToken

class FileStorageTest(unittest.TestCase):
    """This tests the FileStorage class."""
    def setUp(self):
        """Initializes external dependencies"""
        pass
        
    def test_all(self):
        """Tests the storage.all function."""
        token_dict1 = {"access_token": "rrr", "expires_in": 1000}
        token_dict2 = {"access_token": "  ppp", "expires_in": 1000}
        token_dict3 = {"access_token": "  qqqr", "expires_in": 1000}

        new_token1 = AccessToken(**token_dict1)
        new_token2 = AccessToken(**token_dict2)
        new_token3 = AccessToken(**token_dict3)
        tokens = storage.all(AccessToken)
        self.assertEqual(True, any(new_token1.to_dict() == token.to_dict() for token in tokens.values()))
        self.assertEqual(True, any(new_token2.to_dict() == token.to_dict() for token in tokens.values()))
        self.assertEqual(True, any(new_token3.to_dict() == token.to_dict() for token in tokens.values()))
        for token in tokens.values():
            current_token = token
            self.assertEqual(datetime, type(current_token.created_at))
            current_token = token.to_dict()
            self.assertEqual(str, type(current_token["created_at"]))