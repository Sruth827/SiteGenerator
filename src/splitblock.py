import re
from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode, text_node_to_html_node
from textnode import TextNode, TextType
from splitnode import *

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

    if re.findall(r"^`{3}[\s\S]*`{3}$",block):
        return BlockType.CODE

    if re.findall(r"^>", block):
        return BlockType.QUOTE

    lines = [line.strip() for line in block.split("\n") if line.strip()]
    if lines and all(re.match(r"^\d+\.\s", line) for line in lines):
        return BlockType.ORDERED_LIST 
    
    if lines and all(line.startswith(("* ", "- ", "+ ")) for line in lines):
        return BlockType.UNORDERED_LIST
    
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
    block_nodes_created = []
    

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            # Process one heading at a time
            lines = block.strip().split("\n")
            for line in lines:
                if line.startswith("#"):
                    # Count the number of # symbols
                    level = 0
                    for char in line:
                        if char == '#':
                            level += 1
                        else:
                            break
                    
                    # Extract the heading content
                    content = line[level:].strip()
                    
                    # Process inline markdown
                    children = text_to_children(content)
                    
                    # Create heading node with appropriate tag
                    heading_tag = f"h{level}"
                    heading_node = HTMLNode(heading_tag, None, children, None)
                    
                    block_nodes_created.append(heading_node)
            
        
        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            quote_content = []
            for line in lines:
                if line.startswith(">"):
                    content = line[1:].strip()
                    quote_content.append(content) 

            joined = " ".join(quote_content)
            children = text_to_children(joined) 
            quote_node = HTMLNode("blockquote", None, children, None)
            block_nodes_created.append(quote_node)

        elif block_type == BlockType.UNORDERED_LIST:       
            children_list = []
            items = block.split("\n")
            for item in items:
                if item.strip(): #skip empty lines
                    item_content = re.sub(r"^[*\-+]\s+","", item.strip())
                    item_children = text_to_children(item_content)
                    li_node = HTMLNode("li", None, item_children, None)
                    children_list.append(li_node)
            unordered_node = HTMLNode("ul", None, children_list, None)
            block_nodes_created.append(unordered_node)

        elif block_type == BlockType.ORDERED_LIST:
            children_list = []
            items = block.split("\n")
            for item in items:
                if item.strip(): #skip empty lines
                    item_content = re.sub(r'^\d+\.\s+','', item.strip())
                    item_children = text_to_children(item_content)
                    li_node = HTMLNode("li", None, item_children, None)
                    children_list.append(li_node)
            ordered_node = HTMLNode("ol", None, children_list, None)
            block_nodes_created.append(ordered_node)

        elif block_type == BlockType.PARAGRAPH:
            normalized_text = block.replace("\n", " ")
            kids = text_to_children(normalized_text)
            block_node = HTMLNode("p", None , kids, None)
            block_nodes_created.append(block_node)


        elif block_type == BlockType.CODE: 
            #remode ``` from first and last line
            code_content = "\n".join(block.split("\n")[1:-1])

            if not code_content.endswith("\n"):
                code_content += "\n"

            text_code = TextNode(code_content, TextType.TEXT)
            html_text = text_node_to_html_node(text_code)

            code_node = HTMLNode("code", None, [html_text], None)
            block_node = HTMLNode("pre", None, [code_node], None)
            block_nodes_created.append(block_node)

    #add to parent HTMLNode
    parent_node = HTMLNode("div", None, block_nodes_created, None)

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
    # First extract all markdown elements in sequence
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Import these functions if they handle lists of TextNodes
    nodes = split_nodes_bold(nodes)
    nodes = split_nodes_italic(nodes)
    nodes = split_nodes_code(nodes)
    nodes = split_nodes_link(nodes) 
    nodes = split_nodes_image(nodes)
    
    # Convert to HTML nodes
    html_nodes = []
    for node in nodes:
        html_nodes.append(text_node_to_html_node(node))

    return html_nodes
