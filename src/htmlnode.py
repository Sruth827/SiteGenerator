from textnode import TextNode, TextType

def text_node_to_html_node(text_node):
    new_leaf = None

    if text_node.text_type == None:
        raise Exception("no TextType")
    elif text_node.text_type == TextType.TEXT:
        new_leaf = LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        new_leaf = LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        new_leaf = LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
         new_leaf = LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        new_leaf = LeafNode("a", text_node.url, "href")
    elif text_node.text_type == TextType.IMAGE:
        new_leaf = LeafNode("img", "", {"src", "alt"})
    return new_leaf


class HTMLNode():
    def __init__(self, Tag=None, Value=None, Children=None, Props=None):
        self.tag = Tag
        self.value = Value
        self.children = Children if Children else []
        self.props = Props if Props else {}

    def to_html(self):
        if self.children is None or len(self.children) == 0:
            if self.value is None:
                return f"<{self.tag}></{self.tag}>"
            else: 
                return f"<{self.tag}>{self.value}</{self.tag}>"
        else: 
            children_html = ""
            for child in self.children:
                children_html += child.to_html()

            if self.value is None:
                return f"<{self.tag}>{children_html}</{self.tag}>"
            else: 
                return f"<{self.tag}>{self.value}{children_html}</{self.tag}>"
    
    def props_to_html(self):
        return " ".join(f'{key}="{value}"' for key, value in self.props.items())

    def __repr__(self):
        return f"HTMLNODE({self.tag}, {self.value}, {self.children}, {self.props_to_html})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == False:
            raise ValueError("need tag to initialize")
        if self.children == False:
            raise ValueError("need children to initialize")
        tree_string = f"<{self.tag}>{
                            ''.join(child.to_html() for child in self.children)
                            }</{self.tag}>"
        return tree_string




class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__( tag, value, None, props)
        
    def to_html(self):
        if self.value == False:
            raise ValueError()
        if self.tag == None:
            return f"{self.value}"
        return f"<{self.tag}>{self.value}</{self.tag}>"

