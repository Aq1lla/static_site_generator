import re

from textnode import TextType, TextNode
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise Exception("No such type")

    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_node = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_node.extend([node])
            break
        
        temp = node.text.split(delimiter)

        if len(temp) % 2 == 0:
            raise Exception("Invalid Markdown syntax - matching closing delimiter is not found.")
        
        for i in range(len(temp)):
            if i % 2 == 0 or i == 0:
                if temp[i] != "":
                    new_node.extend([TextNode(temp[i], TextType.TEXT)])
            else:
                new_node.extend([TextNode(temp[i], text_type)])
    
    return new_node



def extract_markdown_images(text):
    """
    Function that takes raw markdown text and returns a list of tuples. 
    Each tuple should contain the alt text and the URL of any markdown images.

    Example:
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(extract_markdown_images(text))
    # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
    """

    img_text = re.findall(r"\[(.*?)\]", text)
    alt_text = re.findall(r"\((.*?)\)", text)

    result = []

    for i in range(len(img_text)):
        result.append((img_text[i], alt_text[i]))
    
    return result



def extract_markdown_links(text):
    """
    Function that takes raw markdown text and returns a list of links. 
    Each tuple should contain the anchor text and URL.

    Example:
    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(extract_markdown_links(text))
    # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
    """
    anchor_text = re.findall(r"\[(.*?)\]", text)
    url_text = re.findall(r"\((.*?)\)", text)

    result = []

    for i in range(len(anchor_text)):
        result.append((anchor_text[i], url_text[i]))
    
    return result