#test_add_6.py


import unittest
from parameterized import parameterized
from unittest.mock import patch
from add_6 import Add

class TestAddFive(unittest.TestCase):

    @parameterized.expand([
        ([10, 9], 19),  # nums, expected_result
        ([20, 2], 22),  # nums, expected_result
        ([7, 4], 11),  # nums, expected_result
    ])
    @patch.object(Add, 'get_sum') 
    def test_add_dependent(self, nums, expected_result, mock_get_sum):
        mock_get_sum.return_value = expected_result
        add_instance = Add()
        result = add_instance.add_dependent(nums)

        self.assertEqual(result, expected_result)
        mock_get_sum.assert_called_once_with(nums[0], nums[1])

if __name__ == '__main__':
    unittest.main()
