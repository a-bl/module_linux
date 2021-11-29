import unittest
from calculator import Calculator


class CalculatorTests(unittest.TestCase):

    def test_add(self):
        '''Test case function for addition'''
        self.calc = Calculator()
        result = self.calc.add(4, 7)
        expected = 11
        self.assertEqual(result, expected)

    def test_subtract(self):
        '''Test case function for subtraction'''
        self.calc = Calculator()
        result = self.calc.subtract(10, 5)
        expected = 5
        self.assertEqual(result, expected)


    def test_multiply(self):
        '''Test case function for multiplication'''
        self.calc = Calculator()
        result = self.calc.multiply(3, 7)
        expected = 21
        self.assertEqual(result, expected)

    def test_divide(self):
        '''Test case function for division'''
        self.calc = Calculator()
        result = self.calc.divide(10, 2)
        expected = 5
        self.assertEqual(result, expected)

    @unittest.skip('Some reason')
    def test_div_error(self):
        '''Make sure ZeroDivisionError is raised when necessary'''
        self.calc = Calculator()
        self.assertRaises(ZeroDivisionError, self.calc.divide, 10, 0)


if __name__ == '__main__':
    unittest.main()
