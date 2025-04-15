import re
from enum import Enum

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
