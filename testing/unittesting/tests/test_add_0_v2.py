import unittest
from unittest.mock import MagicMock
from add_0 import add_dependent

class TestAddZero(unittest.TestCase):
    def test_add_dependent(self):
        mock_get_sum = MagicMock()
        mock_get_sum.return_value = 10
        with unittest.mock.patch('add_0.get_sum', mock_get_sum):
            result = add_dependent(3, 4)

        self.assertEqual(result, 10)
        mock_get_sum.assert_called_once_with(3, 4)

if __name__ == '__main__':
    unittest.main()
