#test_add_9.py

import unittest
from unittest import mock
from add_9 import add_dependent

def get_sum_mock(a, b):
    # get_sum function without the long running time.sleep
    return a + b
    
class AddNineTestCase(unittest.TestCase):
    @mock.patch('add_9.get_sum', side_effect=get_sum_mock) 
    def test_add_dependent_v3(self, get_sum_mock):
        result = add_dependent(4, 5)
        self.assertEqual(9, result)
        get_sum_mock.assert_called_with(4, 5)

if __name__ == "__main__":
    unittest.main()
