from enum import Enum

class TextType(Enum):
    TEXT = "Normal Text"
    BOLD = "Bold Text"
    ITALIC = "Italic text"
    CODE = "Code Text" 
    LINK = "Links"
    IMAGE = "Image"

class TextNode():
    def __init__(self, text, text_type, URL=None):
        self.text = text 
        self.text_type = text_type     
        self.url = URL 

        if not isinstance(text_type, TextType):
            raise ValueError(f"Invalid TextType: {text_type}")
        if text_type in {TextType.LINK, TextType.IMAGE} and not URL:
            raise ValueError(f"URL is required for TextType: {text_type}")

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

