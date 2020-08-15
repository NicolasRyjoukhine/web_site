import unittest
from com.nico.webapp.security_flask.password_hashing import password_security



class TestSum(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(password_security(str(6)), '0110', "Should be 0110")

    def test_sum_tuple(self):
        self.assertEqual(sum((1, 2, 2)), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()
