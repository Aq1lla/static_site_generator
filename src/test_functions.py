import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from functions import *


class TestTHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text_link(self):
        node = TextNode("bootcamp", TextType.LINK, "bootcamp.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "bootcamp")
        self.assertEqual(html_node.props, {"href": "bootcamp.com"})

    def test_text_image(self):
        node = TextNode("bootcamp", TextType.IMAGE, "image.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "image.com", "alt": "bootcamp"})
    
    def test_split_node_main(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)])

    def test_split_node_delimiter_on_beggining(self):
        node = TextNode("`code block` on beggining", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("code block", TextType.CODE), TextNode(" on beggining", TextType.TEXT)])

    def test_split_node_delimiter_on_end(self):
        node = TextNode("On end `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("On end ", TextType.TEXT), TextNode("code block", TextType.CODE)])
   
    def test_split_node_multiple(self):
        node = TextNode("This is text with a `code block` word and other `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), 
                                     TextNode("code block", TextType.CODE), 
                                     TextNode(" word and other ", TextType.TEXT), 
                                     TextNode("code block", TextType.CODE), 
                                     TextNode(" word", TextType.TEXT)]
        )

    def test_split_node_delimiter_plain(self):
        node = TextNode("Plain text in here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("Plain text in here", TextType.TEXT)])

    def test_split_node_delimiter_only_delimited(self):
        node = TextNode("`code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("code block", TextType.CODE)])      

    def test_split_node_delimiter_exception(self):
        node = TextNode("On end `code block", TextType.TEXT)
        with self.assertRaisesRegex(Exception, r"^Invalid Markdown syntax - matching closing delimiter is not found\.$"):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("This text contains no markdown images.")
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)
    
    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
           "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"), 
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ],
            matches,
        )
    
    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("This text contains no markdown images.")
        self.assertListEqual([], matches)
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_images_returns_original(self):
        node = TextNode("Plain text with no markdown images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_at_start(self):
        node = TextNode(
            "![first](https://example.com/first.png) followed by text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "https://example.com/first.png"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_at_end(self):
        node = TextNode(
            "Text before image ![last](https://example.com/last.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text before image ", TextType.TEXT),
                TextNode("last", TextType.IMAGE, "https://example.com/last.png"),
            ],
            new_nodes,
        )

    def test_split_images_consecutive_images(self):
        node = TextNode(
            "![one](https://example.com/one.png)![two](https://example.com/two.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("one", TextType.IMAGE, "https://example.com/one.png"),
                TextNode("two", TextType.IMAGE, "https://example.com/two.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_links_no_links_returns_original(self):
        node = TextNode("Plain text with no markdown links.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_at_start(self):
        node = TextNode(
            "[first](https://example.com/first) followed by text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.LINK, "https://example.com/first"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_at_end(self):
        node = TextNode(
            "Text before link [last](https://example.com/last)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text before link ", TextType.TEXT),
                TextNode("last", TextType.LINK, "https://example.com/last"),
            ],
            new_nodes,
        )

    def test_split_links_consecutive_links(self):
        node = TextNode(
            "[one](https://example.com/one)[two](https://example.com/two)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("one", TextType.LINK, "https://example.com/one"),
                TextNode("two", TextType.LINK, "https://example.com/two"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_main(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            result,
        )

    def test_text_to_textnodes_plain_text_returns_original(self):
        text = "Just plain text."
        result = text_to_textnodes(text)
        self.assertListEqual([TextNode("Just plain text.", TextType.TEXT)], result)

    def test_text_to_textnodes_only_bold(self):
        text = "**bold**"
        result = text_to_textnodes(text)
        self.assertListEqual([TextNode("bold", TextType.BOLD)], result)

    def test_text_to_textnodes_image_at_start(self):
        text = "![logo](https://example.com/logo.png) here"
        result = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("logo", TextType.IMAGE, "https://example.com/logo.png"),
                TextNode(" here", TextType.TEXT),
            ],
            result,
        )

    def test_text_to_textnodes_code_and_link(self):
        text = "Call `func()` and open [docs](https://example.com)."
        result = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Call ", TextType.TEXT),
                TextNode("func()", TextType.CODE),
                TextNode(" and open ", TextType.TEXT),
                TextNode("docs", TextType.LINK, "https://example.com"),
                TextNode(".", TextType.TEXT),
            ],
            result,
        )

    def test_text_to_textnodes_unclosed_delimiter_raises_exception(self):
        text = "This is **broken text"
        with self.assertRaisesRegex(Exception, r"^Invalid Markdown syntax - matching closing delimiter is not found\.$"):
            text_to_textnodes(text)


    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_multiline_n(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line




- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    # Tests for block_to_block_type function
    def test_block_to_block_type_heading_h1(self):
        block = "# This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_block_to_block_type_heading_h2(self):
        block = "## This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_block_to_block_type_heading_h6(self):
        block = "###### This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = "```\nprint('Hello')\nprint('World')\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_block_to_block_type_quote_single_line(self):
        block = "> This is a quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_block_to_block_type_quote_multiline(self):
        block = "> This is a quote\n> with multiple lines\n> of content"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_block_to_block_type_unordered_list_single(self):
        block = "- Item one"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UL)

    def test_block_to_block_type_unordered_list_multiple(self):
        block = "- Item one\n- Item two\n- Item three"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UL)

    def test_block_to_block_type_ordered_list_single(self):
        block = "1. Item one"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.OL)

    def test_block_to_block_type_ordered_list_multiple(self):
        block = "1. Item one\n2. Item two\n3. Item three"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.OL)

    def test_block_to_block_type_paragraph_plain_text(self):
        block = "This is a plain paragraph with no special formatting."
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_multiple_lines(self):
        block = "This is a paragraph\nwith multiple lines\nbut no special formatting"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_type_quote_mixed_not_quote(self):
        block = "> This is a quote\nBut this line is not"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list_mixed_not_list(self):
        block = "- Item one\nBut this line is not a list item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading_with_inline_markdown(self):
        md = "# This is a **bold** heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a <b>bold</b> heading</h1></div>",
        )

    def test_unordered_list_with_inline_markdown(self):
        md = "- Item with **bold**\n- Item with _italic_\n- Plain item"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item with <b>bold</b></li><li>Item with <i>italic</i></li><li>Plain item</li></ul></div>",
        )

    def test_ordered_list_with_inline_markdown(self):
        md = "1. First with `code`\n2. Second with **bold**\n3. Third plain"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First with <code>code</code></li><li>Second with <b>bold</b></li><li>Third plain</li></ol></div>",
        )

    def test_quote_with_inline_markdown(self):
        md = "> This is a **important** quote\n> with _multiple_ lines"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a <b>important</b> quote with <i>multiple</i> lines</blockquote></div>",
        )

    def test_multiple_heading_levels(self):
        md = "# Heading 1\n\n## Heading 2\n\n### Heading 3"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>",
        )

    def test_single_item_list(self):
        md = "- Only one item"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Only one item</li></ul></div>",
        )

    def test_quote_single_line(self):
        md = "> A single line quote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>A single line quote</blockquote></div>",
        )

    def test_mixed_blocks_all_types(self):
        md = """# Main Title

This is a paragraph with **bold** and _italic_ text.

- List item one
- List item two

> A quote here

1. Ordered first
2. Ordered second"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<h1>Main Title</h1>", html)
        self.assertIn("<p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p>", html)
        self.assertIn("<ul><li>List item one</li><li>List item two</li></ul>", html)
        self.assertIn("<blockquote>A quote here</blockquote>", html)
        self.assertIn("<ol><li>Ordered first</li><li>Ordered second</li></ol>", html)

if __name__ == "__main__":
    unittest.main()
