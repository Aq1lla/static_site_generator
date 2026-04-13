from textnode import *

def main():
    html = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(html.__repr__())

main()