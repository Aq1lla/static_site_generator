import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType


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
    
    def test_leaf_to_html_p_2(self):
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
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_children(self):
        child_node_one = LeafNode("span", "child")
        child_node_two = ParentNode("div", [child_node_one])
        parent_node = ParentNode("p", [child_node_two])
        self.assertEqual(parent_node.to_html(), "<p><div><span>child</span></div></p>")

    def test_to_html_with_multiple_children(self):
        child_node_one = LeafNode("span", "child1")
        child_node_two = LeafNode("p", "child2")
        child_node_three = LeafNode("div", "child3")
        parent_node = ParentNode("span", [child_node_one, child_node_two, child_node_three])
        self.assertEqual(parent_node.to_html(), "<span><span>child1</span><p>child2</p><div>child3</div></span>")

    def test_parent_to_html_no_children_assertRaises(self):
        node = ParentNode("span", None)
        self.assertRaises(ValueError)
    


if __name__ == "__main__":
    unittest.main()


