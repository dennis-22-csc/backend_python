#test_add_7

import unittest
from add_7 import Add, Op
from unittest.mock import Mock

class TestAddSeven(unittest.TestCase):
    def test_add_op(self):
        # Create a Mock for the Add class
        add_mock = Mock(spec=Add)
        
        # Mock the behavior of add_dependent method
        add_mock.add_dependent.return_value = 11

        # Create an instance of Op
        op = Op()

        # Call the method that internally uses the add_dependent method as well as requires the add object as argument 
        result = op.add_op(add_mock, 19, 12) 
        
        # Check if the expected value is returned
        self.assertEqual(11, result)

        # Check if add_dependent method was called with the correct arguments
        add_mock.add_dependent.assert_called_with(19, 12)

if __name__ == '__main__':
    unittest.main()
