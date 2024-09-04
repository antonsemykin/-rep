import unittest

class TestSum(unittest.TestCase):
    def test_list_int(self):
        """
        Test that it can sum a list of integers
        """
        data = [1, 2, 3]
        result = sum(data)
        self.assertEqual(result, 6)

        self.assertEqual(result+2, 7)
        self.assertEqual(result*3, 18)

if __name__ == '__main__':
    unittest.main()
