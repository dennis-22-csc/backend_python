"""This module tests the file_storage module.
"""

import unittest
import json
from datetime import datetime, timedelta
from models import storage
from models.access_token import AccessToken
from parameterized import parameterized
from models.base_model import BaseModel 
from unittest.mock import patch, Mock


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
        """Tests the all method of FileStorage."""
        
        new_token = AccessToken(**token_dict)
        
        tokens = storage.all(AccessToken)
        self.assertEqual(True, any(new_token.to_dict() == token.to_dict() for token in tokens.values()))
        for token in tokens.values():
            current_token = token
            self.assertEqual(datetime, type(current_token.created_at))
            current_token = token.to_dict()
            self.assertEqual(str, type(current_token["created_at"]))


    def test_new(self):
        """Test new method"""
        my_model = BaseModel()
        test_obj_key = "{}.{}".format(type(my_model).__name__, my_model.id)
        self.assertEqual(my_model, storage._FileStorage__objects[test_obj_key])

    @patch('json.dump')
    @patch('builtins.open')
    @patch('os.path.exists', return_value=True)
    def test_save(self, mock_exists, mock_open, mock_json_dump):
        """ Test save method"""
        BaseModel()

        storage.save()

        mock_open.assert_called_once_with(storage. _FileStorage__file_path, 'w', encoding='utf-8')
        mock_json_dump.assert_called_once()



    
    @patch('json.load')
    @patch('builtins.open')
    @patch('os.path.exists', return_value=True)
    def test_reload(self, mock_exist, mock_open, mock_json_load):
        """ Test reload method"""
        mock_file_content = '{"Client.f44fa2ff-488c-4ce4-969c-2ff0c4883ad7": {"full_name": "Akpotaire Dennis", "email": "denniskoko@gmail.com", "password": "$2b$12$bYhFmW3FqOTiZlKDB3Mhtu4/cam6Vrzra6s/Y.EUyHTl58N5GXoVS", "secret": "sOOI7ycMGI-gHN0VXdrfR95MFu_ThKNj9hS2j2zL60Y", "created_at": "2023-11-20T14:32:30.434849", "updated_at": "2023-11-20T14:32:30.434935", "id": "f44fa2ff-488c-4ce4-969c-2ff0c4883ad7", "__class__": "Client"}}'
        
        mock_file = mock_open(read_data=mock_file_content)
        mock_json_load.return_value = {'Client.f44fa2ff-488c-4ce4-969c-2ff0c4883ad7': {'full_name': 'Akpotaire Dennis', 'email': 'denniskoko@gmail.com', 'password': '$2b$12$bYhFmW3FqOTiZlKDB3Mhtu4/cam6Vrzra6s/Y.EUyHTl58N5GXoVS', 'secret': 'sOOI7ycMGI-gHN0VXdrfR95MFu_ThKNj9hS2j2zL60Y', 'created_at': '2023-11-20T14:32:30.434849', 'updated_at': '2023-11-20T14:32:30.434935', 'id': 'f44fa2ff-488c-4ce4-969c-2ff0c4883ad7', '__class__': 'Client'}}

        storage.reload()

        mock_open.assert_called()
        mock_json_load.assert_called_once()

        loaded_data = storage._FileStorage__objects['Client.f44fa2ff-488c-4ce4-969c-2ff0c4883ad7'].to_dict()
        self.assertEqual(loaded_data['full_name'], 'Akpotaire Dennis')
        self.assertEqual(loaded_data['email'], 'denniskoko@gmail.com')    


    def test_delete(self):
        """Test delete method of FileStorage."""
        my_obj = BaseModel()
        my_obj_key = "{}.{}".format(type(my_obj).__name__, my_obj.id)
        self.assertIn(my_obj_key, storage._FileStorage__objects)
        storage.delete(my_obj)
        self.assertNotIn(my_obj_key, storage._FileStorage__objects)    


    @patch('models.storage.reload')
    def test_close(self, mock_reload):
        """Test if the close method of FileStorage was called."""
        storage.close()
        mock_reload.assert_called_once()


    def test_get(self):
        """Test the get method."""
        obj_mock = Mock()
        my_obj = BaseModel()
        
        mock_get = storage.get(Mock, obj_mock.id)
        model_get = storage.get(BaseModel, my_obj.id)
        self.assertIsNone(mock_get)
        self.assertIsNotNone(model_get)
        self.assertEqual(my_obj, model_get)
