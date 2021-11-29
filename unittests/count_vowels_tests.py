import unittest
import count_vowels


class VowelsTests(unittest.TestCase):

    def test_count(self):
        self.assertEqual(count_vowels.get_res('My black cat'), 2)
        self.assertEqual(count_vowels.get_res('I am studying Python'), 5)

    def test_not_string(self):
        self.assertEqual(count_vowels.get_res("WinPython Control Panel"), 6)
        with self.assertRaises(AttributeError):
            count_vowels.get_res(2)


if __name__ == "__main__":
    unittest.main()