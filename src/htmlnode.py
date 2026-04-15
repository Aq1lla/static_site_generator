class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag                              # A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value                          # A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children                    # A list of HTMLNode objects representing the children of this node
        self.props = props                          # A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        result = ""

        for key, value in self.props.items():
            result += f' {key}="{value}"'
        
        return result
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)


    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        
        if self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("No tag value")
        if self.children == None:
            raise ValueError("No children value")

        result = ""

        for item in self.children:
            result += item.to_html()
        
        return f"<{self.tag}>{result}</{self.tag}>"