import unittest

from main_functions import *


class TestMainFunctions(unittest.TestCase):
    def test_heading(self):
        result = extract_title("# Hello")  
        self.assertEqual(result, "Hello")
        
    def test_extract_title_with_spaces(self):
        self.assertEqual(extract_title("#   Hello World   "), "Hello World")

    def test_extract_title_multiline_first_line(self):
        markdown = "# Title\n\nSome content"
        self.assertEqual(extract_title(markdown), "Title")

    def test_extract_title_multiline_later(self):
        markdown = "Some text\n\n# Title Here\n\nMore text"
        self.assertEqual(extract_title(markdown), "Title Here")

    def test_extract_title_no_space_after_hash(self):
        self.assertEqual(extract_title("#Title"), "Title")

    def test_extract_title_no_header(self):
        with self.assertRaises(Exception):
            extract_title("No header here")

    def test_extract_title_empty_string(self):
        with self.assertRaises(Exception):
            extract_title("")

    def test_extract_title_only_whitespace(self):
        with self.assertRaises(Exception):
            extract_title("   \n\n  ")


if __name__ == "__main__":
    unittest.main()

