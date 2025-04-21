from textnode import TextNode, TextType

def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise TypeError("Expected a TextNode instance")
    if text_node.text_type is None:
        raise ValueError("TextNode must have a valid TextType")
    
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        if not text_node.url:
            raise ValueError("Link TextNode must have a URL")
        return LeafNode("img", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        if not text_node.url:
            raise ValueError("Image TextNode must have a URL")
        return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unsupported TextType: {text_node.text_type}")


class HTMLNode():
    def __init__(self, Tag=None, Value=None, Children=None, Props=None):
        self.tag = Tag
        self.value = Value
        self.children = Children if Children else []
        self.props = Props if Props else {}

    def to_html(self):
        # convert props to a string (e.g., 'href="..." target="_blank"')
        props_string = self.props_to_html()
        props_string = f" {props_string}" if props_string else ""

        # andle self-closing tags if there are no children and no value
        if not self.children and not self.value:
            return f"<{self.tag}{props_string} />"

        # generate children HTML (if any)
        children_html = "".join(child.to_html() for child in self.children)  
        # default to empty list if no children

        # Render the tag
        return f"<{self.tag}{props_string}>{self.value or ''}{children_html}</{self.tag}>"
    
    def props_to_html(self):
        return " ".join(f"{key}='{value}'" for key, value in self.props.items())

    def __repr__(self):
        return f"HTMLNODE({self.tag}, {self.value}, {self.children}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("need tag to initialize")
        if self.children == None:
            raise ValueError("need children to initialize")
        tree_string = f"<{self.tag}>{''.join(child.to_html() for child in self.children)}</{self.tag}>"
        return tree_string




class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__( tag, value, None, props)
        
    def to_html(self):
        if self.value == None:
            raise ValueError()
        
        attributes = ""
        if self.props:
            attributes = " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())

        if self.tag == None:
            return f"{self.value}"
        
        if self.tag in ["img", "br", "hr"]:
            return f"<{self.tag}{attributes}/>"

        return f"<{self.tag}{attributes}>{self.value}</{self.tag}>"

        

