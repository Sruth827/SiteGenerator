
import re
from textnode import TextNode, TextType

def split_node_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        
        lines = node.text.split(delimiter)

        if len(lines) % 2 == 0:
            raise ValueError(f"Invalid Markdown: no matching '{delimiter}'")

        for i, line in enumerate(lines):
            if i%2 == 1:
                new_list.append(TextNode(line, text_type))
            else:
                        
                if line:
                    new_list.append(TextNode(line, TextType.TEXT))
    return new_list

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

