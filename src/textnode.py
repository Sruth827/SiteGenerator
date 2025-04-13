from enum import Enum

class TextType(Enum):
    TEXT = "Normal Text"
    BOLD = "Bold Text"
    ITALIC = "Italic text"
    CODE = "Code Text" 
    LINK = "Links"
    IMAGE = "Image"

class TextNode():
    def __init__(self, text, TextType, URL=None):
        self.text = text 
        self.text_type = TextType     
        self.url = URL 

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text and 
            self.text_type == other.text_type and 
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text},{self.text_type.value}, {self.url})"

