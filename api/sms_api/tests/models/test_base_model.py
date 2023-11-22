"""This module tests the base_model module.
"""

import unittest
from models import storage
from models.base_model import BaseModel
from datetime import datetime
from parameterized import parameterized
from unittest.mock import patch

class BaseModelTest(unittest.TestCase):
    """This tests the BaseModel class."""
       
    @parameterized.expand([
     ("normal", BaseModel()), 
     ("base_model_kwargs", BaseModel().to_dict()), 
     ("partly_empty_kwargs", {"id": "ygqersa.poytdv"}), 
     ("empty_kwargs", {}), 
    ])
    def test_instantiation(self, case_name, my_model):
        """ Test instantiation of BaseModel."""
        if case_name == "normal":
            self._verify_model(my_model)
        elif case_name == "base_model_kwargs":
            my_model_dict = my_model
            self.assertEqual(True, isinstance(my_model_dict["id"], str))
            self.assertEqual(True, isinstance(my_model_dict["created_at"], str))
            self.assertEqual(True, isinstance(my_model_dict["updated_at"] , str))

            new_model = BaseModel(**my_model_dict)
            self._verify_model(new_model)
            self.assertNotIn(my_model, storage.all().values()) # Have been replaced by new model 
        elif case_name == "empty_kwargs" or case_name == "partly_empty_kwargs":
            new_model = BaseModel(**my_model)
            self._verify_model(new_model)

        
        
    def _verify_model(self, model):
        """ Private method used in the instantiation test."""
        self.assertIsInstance(model, BaseModel)
        self.assertEqual(True, hasattr(model, "id"))
        self.assertEqual(True, hasattr(model, "created_at"))
        self.assertEqual(True, hasattr(model, "updated_at"))

        self.assertIsNotNone(model.id) # only relevant to models created using empty kwargs
        self.assertIsNotNone(model.created_at) # only relevant to models created using empty kwargs
        self.assertIsNotNone(model.updated_at) # only relevant to models created using empty kwargs 
        
        self.assertEqual(True, isinstance(model.id, str))
        self.assertEqual(True, isinstance(model.created_at, datetime))
        self.assertEqual(True, isinstance(model.updated_at, datetime))

        self.assertIn(model, storage.all().values())
        

    def test_str(self):
        """ Test str method of BaseModel."""
        my_model = BaseModel()
        my_model_test_str = "[{}] ({}) {}".format("BaseModel", my_model.id, my_model.__dict__)
        self.assertEqual(my_model_test_str,str(my_model))


    def test_to_dict(self):
        """ Test to_dict method of BaseModel."""
        my_model = BaseModel()
        my_model_test_dict = {"id":my_model.id, "created_at": my_model.created_at.isoformat(), "updated_at": my_model.updated_at.isoformat(), "__class__": my_model.__class__.__name__}
        self.assertDictEqual(my_model_test_dict, my_model.to_dict())

    @patch('models.storage.save')
    def test_save(self, mock_save):
        """ Test save method of BaseModel."""
        base_model = BaseModel()

        created_at_on_create = base_model.created_at
        updated_at_on_create = base_model.updated_at

        base_model.save()

        created_at_on_update = base_model.created_at
        updated_at_on_update = base_model.updated_at

        self.assertLess(updated_at_on_create, updated_at_on_update)
        self.assertEqual(created_at_on_create, created_at_on_update)
