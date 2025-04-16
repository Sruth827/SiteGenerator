import re
from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode, text_node_to_html_node
from textnode import TextNode, TextType
from splitnode import split_node_delimiter, extract_markdown_links, extract_markdown_images

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(block):
    if re.findall(r"#{1,6} [^\n]+", block):
        return BlockType.HEADING
    elif re.findall(r"^`{3}[\s\S]*`{3}$",block):
        return BlockType.CODE
    elif re.findall(r"^>", block):
        return BlockType.QUOTE
    elif re.findall(r"^- ", block):
        return BlockType.UNORDERED_LIST
    elif re.findall(r"^(\d+)\. .+$", block):
        return BlockType.ORDERED_LIST
    else: 
        return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    # First, normalize line endings and strip
    markdown = markdown.strip()
    
    # Split by one or more blank lines (a blank line can contain whitespace)
    blocks = re.split(r'\n\s*\n', markdown)
    
    # Process blocks to remove empty ones
    result = []
    for block in blocks:
        if block.strip():  # Only add non-empty blocks
            result.append(block)
    
    return result


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_node = HTMLNode("div", None, None, [])
    

    for block in blocks:
        block_type = block_to_block_type(block)

        #HTMLNode created based on BlockType
        if block_type == BlockType.HEADING:
            count = count_hashes_at_start(block)
            cleaned_text = block[count:].strip()
            block_node = HTMLNode(f"h{count}", None, None, [])
        elif block_type == BlockType.QUOTE:
            block_node = HTMLNode("blockquote", None, None, [])
        elif block_type == BlockType.UNORDERED_LIST:
            block_node = HTMLNode("ul", None, None, [list_node])
            list_node = HTMLNode("li",None, None, [])
        elif block_type == BlockType.ORDERED_LIST:
            block_node = HTMLNode("ol", None, None, [list_node])
            list_node = HTMLNode("li", None, None, [])
        elif block_type == BlockType.PARAGRAPH:
            block_node = HTMLNode("p", None, None, [])
        elif block_type == BlockType.CODE: 
            code_node = HTMLNode("code", None, None, [])
            block_node = HTMLNode("pre", None, None, [code_node])
            text_node = TextNode(block, TextType.TEXT)
            code_node.children = [text_node_to_html_node(text_node)]
            block_node.children = [code_node]

        
        #add to parent HTMLNode
        parent_node.children.append(block_node)

    return parent_node

    
def count_hashes_at_start(s):
    # Use a loop or regex to count leading `#`
    count = 0
    for char in s:
        if char == '#':
            count += 1
        else:
            break  # Stop counting once a non-`#` character is encountered
    return count

def text_to_children(text):
    text_node = TextNode(text, TextType.TEXT)
    
    #split by delimiter to seperate bold, ital, code 
    nodes = [text_node]
    nodes = split_node_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_node_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_node_delimiter(nodes, "`", TextType.CODE)

    #extract links and images 
    node = extract_markdown_images(nodes)
    node = extract_markdown_images(nodes)

    #convert to HTMLNodes
    html_nodes = []
    for node in nodes:
        html_nodes.append(text_node_to_html_node(node))

    return html_nodes
