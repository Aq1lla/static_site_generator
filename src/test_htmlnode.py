import unittest

from htmlnode import HTMLNode


class TestTHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "This is a text node", [], {"href": "https://www.google.com", "target": "_blank",})
        expected = ' href="https://www.google.com" target="_blank"'
        print(node.props_to_html())
        self.assertEqual(node.props_to_html(), expected)

    def test_is_none(self):
        node = HTMLNode("p", "This is a text node")
        self.assertIsNone(node.children)

    def test_not_none(self):
        node = HTMLNode("p", "This is a text node", [], {"href": "https://www.google.com", "target": "_blank",})
        self.assertIsNotNone(node.children)

    def test_is_instance(self):
        node = HTMLNode("p", "This is a text node", [], {"href": "https://www.google.com", "target": "_blank",})
        self.assertIsInstance(node, HTMLNode)


if __name__ == "__main__":
    unittest.main()



    