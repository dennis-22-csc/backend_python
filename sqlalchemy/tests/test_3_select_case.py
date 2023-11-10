"""This module tests the functions in the 3_select_case module."""

import unittest
from models import Customer 
from test_config import Session

insert_customers_from_dict_list = __import__("2_multiple_data_insert").insert_customers_from_dict_list
get_customers = __import__("3_select_case").get_customers_dynamically_generating_age_group_data_for_each_customer
create_tables = __import__('create_test_tables').create_tables
delete_tables = __import__('delete_all_test_tables').delete_all_tables

class ThreeSelectCaseTestCase(unittest.TestCase):
    """This will test the get_customers_dynamically_generating_age_group_data_for_each_customer
function in the 3_select_case module."""

    def setUp(self):
        """Initializes external dependencies."""
        self.db_session = Session()
        create_tables()

    def tearDown(self):
        """Removes no longer needed objects."""
        self.db_session.close()
        delete_tables()
       
    def test_get_customers_when_data_has_not_been_inserted(self):
        """Test the function when no customer data has been added."""
        result = get_customers(self.db_session)
        self.assertEqual([], result)

    def test_get_customers_for_age_group(self):
        """Test the function when data has been added to see if the returned data is a list of customer objects having an age_group property."""
        customers = [ 
							{"name": "Alice", "age": 25},
   						{"name": "Bob", "age": 30},
   						{"name": "Charlie", "age": 22},
   						{"name": "David", "age": 35},
   						{"name": "Eve", "age": 28},
   						{"name": "Frank", "age": 32},
   						{"name": "Grace", "age": 27},
   						{"name": "Eve", "age": 28},
   						{"name": "Dennis", "age": 22},
   						{"name": "Alimat", "age": 17},
   						{"name": "Hilda", "age": 25},
   						{"name": "Chibuike", "age": 30},
   						{"name": "Nathan", "age": 22},
   						{"name": "Oluwaseun", "age": 35}
  		] 
        insert_customers_from_dict_list(self.db_session, customers)
        result = get_customers(self.db_session)
        self.assertEqual(True, all(hasattr(customer, 'age_group') for customer in result))

    def test_get_customers_for_invalid_session_object(self):
        """Test the function to see if it returns an error message when invalid session object is supplied as input."""
        customer = Customer(name="Dennis", age=20)
        db_session = customer
        result = get_customers(db_session)
        self.assertIsInstance(result, str)
      
