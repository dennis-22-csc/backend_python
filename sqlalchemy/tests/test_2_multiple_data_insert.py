"""This module tests the functions in the 2_multiple_data_insert module."""

import unittest
import os
from models import Customer 
from test_config import Session

insert_customers_from_dict_list = __import__("2_multiple_data_insert").insert_customers_from_dict_list
create_tables = __import__('create_test_tables').create_tables
delete_tables = __import__('delete_all_test_tables').delete_all_tables

class TwoMultipleDataInsertTestCase(unittest.TestCase):
    """This will test the insert_customers_from_dict_list function in the 2_multiple_data_insert module."""

    def setUp(self):
        """Initializes external dependencies."""
        self.db_session = Session()
        create_tables()

    def tearDown(self):
        """Removes no longer needed objects."""
        self.db_session.close()
        delete_tables()
        open("database.log", "w").close() # Empty the file


    def test_insert_multiple_data_for_correct_input(self):
        """Test insert_customers_from_dict_list function for correct input."""
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
        result = insert_customers_from_dict_list(self.db_session, customers)
        self.assertEqual("Customers added successfully", result)
        
    def test_insert_multiple_data_when_customers_dicts_are_in_tuple_instead_of_list(self):
        """Test insert_customers_from_dict_list function when customer info dictionaries are in a tuple instead of a list."""
        customers = (
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
  		)
        result = insert_customers_from_dict_list(self.db_session, customers)
        self.assertEqual(True, result.startswith("Error occurred"))

    def test_insert_multiple_data_when_one_or_more_customer_info_are_in_list_instead_of_dict(self):
        """Test insert_customers_from_dict_list function when one or more customer info are in a list instead of a dictionary."""
        customers = [ 
							{"name": "Alice", "age": 25},
   						{"name": "Bob", "age": 30},
   						["name", "Charlie", "age", 22],
   						{"name": "David", "age": 35},
   						{"name": "Eve", "age": 28},
   						{"name": "Frank", "age": 32},
   						{"name": "Grace", "age": 27},
   						{"name": "Eve", "age": 28},
   						{"name": "Dennis", "age": 22},
   						{"name": "Alimat", "age": 17},
   						{"name": "Hilda", "age": 25},
   						{"name": "Chibuike", "age": 30},
   						["name", "Nathan", "age", 22],
   						{"name": "Oluwaseun", "age": 35}
  		] 
        result = insert_customers_from_dict_list(self.db_session, customers)
        customer_dict1 = ["name", "Charlie", "age", 22]
        customer_dict2 = ["name", "Nathan", "age", 22]
        with open('database.log', 'r') as log_file:
            log_content = log_file.read()
            self.assertIn(f"{customer_dict1} is not a dictionary.", log_content)
            self.assertIn(f"{customer_dict2} is not a dictionary.", log_content)
            self.assertEqual("Added all customers except 2. Check the database log for more details.", result)
        
           
    def test_insert_multiple_data_when_one_or_more_customer_info_dict_contains_the_wrong_key(self):
        """Test insert_customers_from_dict_list function when one or more customer info dictionaries contains the wrong key."""
        customers = [ 
							{"name": "Alice", "age": 25},
   						{"username": "Bob", "age": 30},
   						{"name": "Charlie", "age": 22},
   						{"name": "David", "age": 35},
   						{"name": "Eve", "age": 28},
   						{"name": "Frank", "score": 32},
   						{"name": "Grace", "age": 27},
   						{"name": "Eve", "age": 28},
   						{"name": "Dennis", "age": 22},
   						{"name": "Alimat", "age": 17},
   						{"name": "Hilda", "age": 25},
   						{"petname": "Chibuike", "age": 30},
   						{"name": "Nathan", "age": 22},
   						{"name": "Oluwaseun", "age": 35}
  		] 
        result = insert_customers_from_dict_list(self.db_session, customers)
        customer_dict1 = {"username": "Bob", "age": 30}
        customer_dict2 = {"name": "Frank", "score": 32}
        customer_dict3 = {"petname": "Chibuike", "age": 30}
        
        with open('database.log', 'r') as log_file:
            log_content = log_file.read()
            self.assertIn(f"{customer_dict1} doesn't have a correct key.", log_content)
            self.assertIn(f"{customer_dict2} doesn't have a correct key.",log_content)
            self.assertIn(f"{customer_dict3} doesn't have a correct key.", log_content)
            self.assertEqual("Added all customers except 3. Check the database log for more details.", result)
        
