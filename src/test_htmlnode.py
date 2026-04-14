import unittest

from htmlnode import HTMLNode, LeafNode


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
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
    
    def test_leaf_to_html_p_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')    
        
    def test_leaf_to_html_p_assertRaises(self):
        node = LeafNode("a", None, {"href": "https://www.google.com"})
        self.assertRaises(ValueError)
    
    def test_leaf_to_html_notag(self):
        node = LeafNode(None, "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "Click me!")  

if __name__ == "__main__":
    unittest.main()


