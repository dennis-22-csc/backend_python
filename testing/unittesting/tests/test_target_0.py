#test_target_0.py

import unittest
from unittest.mock import patch
from target_0 import method, Target 

class TargetZeroTestCase(unittest.TestCase):
    @patch.object(Target,  "apply", autospec=True)
    def test_method(self, mock_apply):
        target = Target()
        
        method(target, "Dennis", 1)

        mock_apply.assert_called_with(target, "Dennis", 1)


if __name__ == "__main__":
    unittest.main()
