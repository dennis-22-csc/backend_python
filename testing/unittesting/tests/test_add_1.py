#test_add_1.py

import unittest
from unittest import mock
from add_1 import add_dependent

class AddOneTestCase(unittest.TestCase):
    @mock.patch('add_1.get_num2')
    @mock.patch('add_1.get_num1')
    @mock.patch('add_1.get_sum')
    def test_add_dependent(self, mock_get_sum, mock_get_num1, mock_get_num2):
        mock_get_sum.return_value = 9
        mock_get_num1.return_value = 4
        mock_get_num2.return_value = 5
        result = add_dependent()
        self.assertEqual(9, result)
        mock_get_sum.assert_called_with(4, 5)

if __name__ == "__main__":
    unittest.main()
