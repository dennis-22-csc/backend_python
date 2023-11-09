""" 

This module defines unit tests for the create_user function in the 0_insert_data module. 

Attributes:
	create_user (func): references the create_user function. 
	
Functions:
	test_create_user_when_user_is_correct(self): Tests the create_user function when
        the user parameter is correctly passed. 
    test_create_user_when_user_is_missing_username_parameter(self): Tests 
        the create_user function when user is missing the username parameter. 
    test_create_user_when_user_is_missing_profile_parameter(self): Tests 
        the create_user function when user is missing the profile parameter. 

"""

import unittest
from models import User, Profile
from config import Session

create_user = __import__('0_insert_data').create_user

class DatabaseCreateUserFunctionTestCase(unittest.TestCase):
    """This will test the create_user function given various inputs. 
	"""

    def setUp(self):
        """Initializes external dependencies"""
        self.db_session = Session()

    def teardown(self):
        """Closes open objects"""
        self.db_session.close()

    def test_create_user_when_user_is_correct(self):
        """Test create_user function when user argument is correctly supplied"""
        new_user = User(username='dennis', profile=Profile(full_name='Akpotaire Dennis'))
        result = create_user(self.db_session, new_user)
        self.assertEqual(1, result)

    def test_create_user_when_user_is_missing_username_parameter(self):
        """Test create_user function when user argument is missing username parameter"""
        new_user = User(profile=Profile(full_name='Alimat Abimbola'))
        result = create_user(self.db_session, new_user)
        self.assertEqual(-1, result)

    def test_create_user_when_user_is_missing_profile_parameter(self):
        new_user = User(username='oluwaseun', )
        result = create_user(self.db_session, new_user)
        self.assertEqual(-1, result)

if __name__ == "__main__":
    unittest.main()
