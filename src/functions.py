import re

from textnode import TextType, TextNode
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    """
    Function that handle each type of the TextType enum. If it gets a TextNode that is none of those types, it should raise an exception. Otherwise, it should return a new LeafNode object.

    TextType.TEXT: This should return a LeafNode with no tag, just a raw text value.
    TextType.BOLD: This should return a LeafNode with a "b" tag and the text
    TextType.ITALIC: "i" tag, text
    TextType.CODE: "code" tag, text
    TextType.LINK: "a" tag, anchor text, and "href" prop
    TextType.IMAGE: "img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)
    """
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

    alt_text = re.findall(r"\[(.*?)\]", text)
    url_text = re.findall(r"\((.*?)\)", text)

    result = []

    for i in range(len(alt_text)):
        result.append((alt_text[i], url_text[i]))
    
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



def split_nodes_image(old_nodes):
    """
    Example:
    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    # [
    #     TextNode("This is text with a link ", TextType.TEXT),
    #     TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
    #     TextNode(" and ", TextType.TEXT),
    #     TextNode(
    #         "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
    #     ),
    # ]
    """
    new_node = []

    for node in old_nodes:
        
        images = extract_markdown_images(node.text)

        if len(images) == 0:
            new_node.append(node)

        check_text = node.text
        check_imgs = 0

        while check_imgs < len(images):
            splits = check_text.split(f"![{images[check_imgs][0]}]({images[check_imgs][1]})", 1)

            if splits[0] != "":
                new_node.append(TextNode(splits[0], TextType.TEXT))

            new_node.append(
                TextNode(images[check_imgs][0], TextType.IMAGE, images[check_imgs][1])
            )
            check_text = splits[1]
            check_imgs += 1

        if len(images) > 0 and check_text != "":
            new_node.append(TextNode(check_text, TextType.TEXT))
   
    return new_node



def split_nodes_link(old_nodes):
    new_node = []
    
    for node in old_nodes:
        
        links = extract_markdown_links(node.text)

        if len(links) == 0:
            new_node.append(node)

        check_text = node.text
        check_links = 0

        while check_links < len(links):
            splits = check_text.split(f"[{links[check_links][0]}]({links[check_links][1]})", 1)

            if splits[0] != "":
                new_node.append(TextNode(splits[0], TextType.TEXT))

            new_node.append(
                TextNode(links[check_links][0], TextType.LINK, links[check_links][1])
            )
            check_text = splits[1]
            check_links += 1

        if len(links) > 0 and check_text != "":
            new_node.append(TextNode(check_text, TextType.TEXT))
   
    return new_node


def text_to_textnodes(text):
    """
    Function that can convert a raw string of markdown-flavored text into a list of TextNode objects.

    Example:
    text = This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)
    result = text_to_textnodes(text)
    # [
    #       TextNode("This is ", TextType.TEXT),
    #       TextNode("text", TextType.BOLD),
    #       TextNode(" with an ", TextType.TEXT),
    #       TextNode("italic", TextType.ITALIC),
    #       TextNode(" word and a ", TextType.TEXT),
    #       TextNode("code block", TextType.CODE),
    #       TextNode(" and an ", TextType.TEXT),
    #       TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    #       TextNode(" and a ", TextType.TEXT),
    #       TextNode("link", TextType.LINK, "https://boot.dev"),
    # ]
    """
    result = text_node_to_html_node(text)
