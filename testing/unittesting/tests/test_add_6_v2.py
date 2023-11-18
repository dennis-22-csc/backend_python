import unittest
from add_6 import Add
from unittest.mock import MagicMock

class TestAddSix(unittest.TestCase):
    def test_add_dependent(self):
        sum = Add()
        sum.get_sum = MagicMock(return_value=15)
        result = sum.add_dependent([9, 2])
        self.assertEqual(15, result)
        sum.get_sum.assert_called_with(9, 2)
		
if __name__ == '__main__':
    unittest.main()
