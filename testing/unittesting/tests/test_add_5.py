#test_add_5.py


import unittest
from parameterized import parameterized
from unittest.mock import patch
from add_5 import Add

class TestAddFive(unittest.TestCase):

    @parameterized.expand([
        (10, 9, 19),  # num1, num2, expected_result
        (20, 2, 22),  # num1, num2, expected_result
        (7, 4, 11),  # num1, num2, expected_result
    ])
    @patch.object(Add, 'get_sum') 
    def test_add_dependent(self, num1, num2, expected_result, mock_get_sum):
        mock_get_sum.return_value = expected_result
        add_instance = Add()
        result = add_instance.add_dependent(num1, num2)

        self.assertEqual(result, expected_result)
        mock_get_sum.assert_called_once_with(num1, num2)

if __name__ == '__main__':
    unittest.main()
