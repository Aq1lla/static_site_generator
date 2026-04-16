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