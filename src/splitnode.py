
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
            if i % 2 == 1:
                new_list.append(TextNode(line, text_type))
                        
            elif line:
                new_list.append(TextNode(line, TextType.TEXT))

            elif not line.strip():
                continue
    
    return new_list


def extract_markdown_bold(text):
    matches = []
    for match in re.finditer(r"\*\*(.*)\*\*", text):
        matches.append((match.group(1), match.start(), match.end()))
    return matches

def extract_markdown_italic(text):
    matches = []
    for match in re.finditer(r"_(.*)_", text):
        matches.append((match.group(1), match.start(), match.end()))
    return matches

def extract_markdown_code(text):
    matches = []
    for match in re.finditer(r"`(.*)`", text):
        matches.append((match.group(1), match.start(), match.end()))
    return matches 

def extract_markdown_images(text):
    matches = []
    pattern = r"!\[(.*?)\]\((.*?)\)"
    for match in re.finditer(pattern, text):
        alt_text = match.group(1)
        url = match.group(2)
        matches.append((alt_text, url))  # Just return text and URL
    return matches

def extract_markdown_links(text):
    matches = []
    pattern = r"\[(.*?)\]\((.*?)\)"
    for match in re.finditer(pattern, text):
        link_text = match.group(1)
        url = match.group(2)
        matches.append((link_text, url))  # Just return text and URL
    return matches

def split_nodes_bold(old_nodes):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        matches = extract_markdown_bold(node.text)
        if not matches:
            new_list.append(node)
            continue

        text = node.text
        for bold_text, start, end in matches:
            # Extract the part before the match
            before_text = text[:start]
            # Update text to be everything after the match
            text = text[end:]
            
            if before_text:
                new_list.append(TextNode(before_text, TextType.TEXT))
            new_list.append(TextNode(bold_text, TextType.BOLD))
        
        # Add any remaining text
        if text:
            new_list.append(TextNode(text, TextType.TEXT))
                        
    return new_list


def split_nodes_italic(old_nodes):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        matches = extract_markdown_italic(node.text)
        if not matches:
            new_list.append(node)
            continue

        text = node.text
        for italic_text, start, end in matches:
            # Extract the part before the match
            before_text = text[:start]
            # Update text to be everything after the match
            text = text[end:]
            
            if before_text:
                new_list.append(TextNode(before_text, TextType.TEXT))
            new_list.append(TextNode(italic_text, TextType.ITALIC))
        
        # Add any remaining text
        if text:
            new_list.append(TextNode(text, TextType.TEXT))
                        
    return new_list


def split_nodes_code(old_nodes):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        matches = extract_markdown_code(node.text)
        if not matches:
            new_list.append(node)
            continue

        text = node.text
        for code_text, start, end in matches:
            # Extract the part before the match
            before_text = text[:start]
            # Update text to be everything after the match
            text = text[end:]
            
            if before_text:
                new_list.append(TextNode(before_text, TextType.TEXT))
            new_list.append(TextNode(code_text, TextType.CODE))
        
        # Add any remaining text
        if text:
            new_list.append(TextNode(text, TextType.TEXT))
                        
    return new_list


def split_nodes_image(nodes):
    result = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
            
        matches = extract_markdown_images(node.text)
        if not matches:
            result.append(node)
            continue
        
        # Start with the original text
        remaining_text = node.text
        current_idx = 0
        
        while matches and remaining_text:
            alt_text, url = matches[0]
            # Construct the full markdown image syntax
            markdown = f"![{alt_text}]({url})"
            # Find position of this markdown in the remaining text
            start_idx = remaining_text.find(markdown)
            
            if start_idx == -1:
                # This match is no longer in the remaining text
                matches.pop(0)
                continue
            
            # Add text before the image if any
            if start_idx > 0:
                result.append(TextNode(remaining_text[:start_idx], TextType.TEXT))
            
            # Add the image node
            result.append(TextNode(alt_text, TextType.IMAGE, url))
            
            # Update remaining_text to be everything after the markdown
            remaining_text = remaining_text[start_idx + len(markdown):]
            matches.pop(0)
        
        # Add any remaining text
        if remaining_text:
            result.append(TextNode(remaining_text, TextType.TEXT))
    
    return result

def split_nodes_link(nodes):
    result = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
            
        matches = extract_markdown_links(node.text)
        if not matches:
            result.append(node)
            continue
        
        # Start with the original text
        remaining_text = node.text
        current_idx = 0

        while matches and remaining_text:
            alt_text, url = matches[0]
            # Construct the full markdown image syntax
            markdown = f"[{alt_text}]({url})"
            # Find position of this markdown in the remaining text
            start_idx = remaining_text.find(markdown)
            
            if start_idx == -1:
                # This match is no longer in the remaining text
                matches.pop(0)
                continue
            
            # Add text before the image if any
            if start_idx > 0:
                result.append(TextNode(remaining_text[:start_idx], TextType.TEXT))
            
            # Add the image node
            result.append(TextNode(alt_text, TextType.LINK, url))
            
            # Update remaining_text to be everything after the markdown
            remaining_text = remaining_text[start_idx + len(markdown):]
            matches.pop(0)
        
        # Add any remaining text
        if remaining_text:
            result.append(TextNode(remaining_text, TextType.TEXT))
    
    return result
 

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_bold(nodes)
    nodes = split_nodes_italic(nodes)
    nodes = split_nodes_code(nodes)
    return nodes
