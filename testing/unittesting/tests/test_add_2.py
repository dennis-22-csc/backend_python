#test_add_2.py

import unittest
from unittest import mock
from add_2 import add_dependent

class AddTwoTestCase(unittest.TestCase):
    @mock.patch('add_2.get_sum')
    def test_add_dependent(self, mock_get_sum):
        mock_get_sum.return_value = 9
        result = add_dependent()
        self.assertEqual(9, result)
        mock_get_sum.assert_called_with(4, 5)

if __name__ == "__main__":
    unittest.main()
