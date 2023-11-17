#test_add_4.py

import unittest
from unittest.mock import patch
from add_4 import Add

class AddFourTestCase(unittest.TestCase):

    @patch.object(Add, 'get_sum', return_value=19) 
    def test_add_dependent(self, mock_get_sum):
        add_instance = Add()
        result = add_instance.add_dependent()

        self.assertEqual(result, 19)
        mock_get_sum.assert_called_once_with(4, 5)

if __name__ == '__main__':
    unittest.main()
