from htmlnode import HTMLNode

class LeafNode():
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(self, tag, value, None, props)
        
    def to_html(self):
        if self.value == False:
            raise ValueError()
        if self.tag == None:
            return f"{self.value}"
        return f"<{self.tag}>{self.value}<{self.tag}>"


