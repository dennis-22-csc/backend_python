#test_add_8

import unittest
from add_8 import Add, Op
from unittest.mock import Mock

class TestAddEight(unittest.TestCase):
    def test_add_op(self):
        # Create a Mock for the Add class
        add_mock = Mock(spec=Add)
        
        # Mock the behavior of add_dependent method to raise an exception 
        add_mock.add_dependent.side_effect = ValueError("Num1 and Num2 needs to be integers")

        # Create an instance of Op
        op = Op()

        # Call the method that internally uses the add_dependent method as well as requires the add object as argument 
        result = op.add_op(add_mock, 9, "12") 
        
        # Check if the expected value 0 is returned
        self.assertEqual(0, result)

        # Check if add_dependent method was called with the correct arguments
        add_mock.add_dependent.assert_called_with(9, "12")

if __name__ == '__main__':
    unittest.main()
