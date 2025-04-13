

class HTMLNode():
    def __init__(self, Tag=None, Value=None, Children=None, Props=None):
        self.tag = Tag
        self.value = Value
        self.children = Children
        self.props = Props if Props else {}

    def to_html(self):
        raise NotImplementedError() 
    
    def props_to_html(self):
        return " ".join(f'{key}="{value}"' for key, value in self.props.items())

    def __repr__(self):
        return f"HTMLNODE({self.tag}, {self.value}, {self.children}, {self.props_to_html})"


