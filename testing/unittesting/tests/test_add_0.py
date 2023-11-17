#test_add_0.py

import unittest
from unittest import mock
from add_0 import add_independent, add_dependent

class AddZeroTestCase(unittest.TestCase):

    @mock.patch('add_0.get_sum')
    def test_add_dependent(self, mock_get_sum):
        mock_get_sum.return_value = 9
        result = add_dependent(4, 5)
        self.assertEqual(9, result)
        mock_get_sum.assert_called_with(4, 5)
    
    def test_add_independent(self):
        result = add_independent(4, 5)
        self.assertEqual(9, result)

if __name__ == "__main__":
    unittest.main()
