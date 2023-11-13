"""
This module tests the functions in the 1_get_data module."""

import unittest
from models import User, Profile
from test_config import Session

create_user = __import__("0_insert_data").create_user
get_users = __import__("1_get_data").get_users
get_profiles = __import__("1_get_data").get_profiles
create_tables = __import__('create_test_tables').create_tables
delete_tables = __import__('delete_all_test_tables').delete_all_tables

class OneGetDataModuleTestCase(unittest.TestCase):
    """This will test the functions in the 1_get_data module given various inputs. 
	"""

    def setUp(self):
        """Initializes external dependencies"""
        self.db_session = Session()
        delete_tables()
        create_tables()

        
    def test_get_users_when_data_has_not_been_inserted(self):
        """Test get users when a user has not been inserted in the database."""
        result = get_users(self.db_session)
        self.assertEqual([], result)
        self.db_session.close()
        delete_tables()

    def test_get_users_when_data_has_been_inserted(self):
        """Test get users when a user has been inserted in the database."""
        new_user = User(username='mark', profile=Profile(full_name='Mark Anthony'))
        create_user(self.db_session, new_user)
        result = get_users(self.db_session)
        self.assertEqual(new_user, result[0])
        self.db_session.close()
        delete_tables()

        
    def test_get_users_for_invalid_session_object(self):
        """Test get users when an invalid session object is passed as input."""
        new_user = User(username='chiddy', profile=Profile(full_name='Chidiebere Onoke'))
        db_session = new_user
        result = get_users(db_session)
        self.assertIsInstance(result, str)
        self.db_session.close()
        delete_tables()

    def test_get_profiles_when_data_has_not_been_inserted(self):
        """Test get profiles when a user has not been inserted in the database."""
        result = get_profiles(self.db_session)
        self.assertEqual([], result)
        self.db_session.close()
        delete_tables()

    def test_get_profiles_when_data_has_been_inserted(self):
        """Test get profiles when a user has been inserted in the database.""" 
        new_user = User(username='mark', profile=Profile(full_name='Mark Anthony'))
        create_user(self.db_session, new_user)
        result = get_profiles(self.db_session)
        self.assertEqual(new_user.profile, result[0])
        self.db_session.close()
        delete_tables()

    def test_get_profiles_for_invalid_session_object(self):
        """Test get profiles when an invalid session object is supplied as input."""
        new_profile = Profile(full_name='Chidiebere Onoke')
        db_session = new_profile
        result = get_profiles(db_session)
        self.assertIsInstance(result, str)
        self.db_session.close()
        delete_tables()

if __name__ == "__main__":
    unittest.main()
