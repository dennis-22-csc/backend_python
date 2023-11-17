#test_add_3.py

import unittest
import add_3
from unittest import mock
from add_3 import add_dependent

class AddThreeTestCase(unittest.TestCase):
    @mock.patch('add_3.num1', 10)
    @mock.patch('add_3.num2', 9)
    @mock.patch('add_3.get_sum')
    def test_add_dependent(self, mock_get_sum):
        self.assertEqual(10, add_3.num1) 
        self.assertEqual(9, add_3.num2)
        mock_get_sum.return_value = 19
        result = add_dependent()
        self.assertEqual(19, result)
        mock_get_sum.assert_called_with(10, 9)

if __name__ == "__main__":
    unittest.main()