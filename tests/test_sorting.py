import unittest
from app.sorting import sort_numbers

class TestSorting(unittest.TestCase):
    def test_sort_numbers(self):
        # Test sorting with a standard list of numbers
        result = sort_numbers([10, 1, 25, 3])
        self.assertEqual(result, [25, 10, 3, 1])

        # Test sorting with negative numbers
        result = sort_numbers([-1, -3, -2, 0])
        self.assertEqual(result, [0, -1, -2, -3])

        # Test sorting with an already sorted list
        result = sort_numbers([30, 20, 10, 0])
        self.assertEqual(result, [30, 20, 10, 0])

        # Test sorting with an empty list
        result = sort_numbers([])
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
