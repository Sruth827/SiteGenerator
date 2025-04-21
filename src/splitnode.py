
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
    for match in re.finditer(r"\*\*(.*?)\*\*", text):
        matches.append((match.group(1), match.start(), match.end()))
    return matches

def extract_markdown_italic(text):
    matches = []
    for match in re.finditer(r"_(.*)_", text):
        matches.append((match.group(1), match.start(), match.end()))
    return matches

def extract_markdown_code(text):
    matches = []
    # Use a regex that finds each code block separately
    pattern = r"`([^`]+)`"
    
    for match in re.finditer(pattern, text):
        code_text = match.group(1)
        start = match.start()
        end = match.end()
        matches.append((code_text, start, end))
    
    return matches

def extract_markdown_images(text):
    matches = []
    pattern = r"(!)?\[([^\]]+)\]\(([^)]+)\)"
    for match in re.finditer(pattern, text):
        is_image = match.group(1)
        alt_text = match.group(2)
        url = match.group(3)
        matches.append((is_image, alt_text, url))  # Just return text and URL
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

        # Sort matches by start position to ensure we process them in order
        matches.sort(key=lambda x: x[1])
        
        curr_index = 0
        for code_text, start, end in matches:
            # Add text before the code block
            if start > curr_index:
                before_text = node.text[curr_index:start]
                new_list.append(TextNode(before_text, TextType.TEXT))
            
            # Add the code block
            new_list.append(TextNode(code_text, TextType.CODE))
            
            # Update current index
            curr_index = end
        
        # Add any remaining text after the last match
        if curr_index < len(node.text):
            remaining_text = node.text[curr_index:]
            new_list.append(TextNode(remaining_text, TextType.TEXT))
                        
    return new_list


def split_nodes_image(old_nodes):
    new_list = []  # Modified list of nodes

    for node in old_nodes:
        # If the node is not of type TEXT, add it directly to the new list
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue

        text = node.text
        pattern = r"(!)?\[([^\]]+)\]\(([^)]+)\)"
        last_idx = 0

        # Use regex to find all matches for markdown images or links
        for match in re.finditer(pattern, text):
            is_image = match.group(1) == "!"  # True for images, False for links
            label = match.group(2)  # Alt text or link text
            url = match.group(3)  # URL
            start_idx = match.start()

            # Add preceding text as a TEXT node
            if start_idx > last_idx:
                new_list.append(TextNode(text[last_idx:start_idx], TextType.TEXT))

            # Add image nodes (only if `is_image` is True)
            if is_image:
                new_list.append(TextNode(label, TextType.IMAGE, url))

            last_idx = match.end()

    # Add any remaining text as a TEXT node
        if last_idx < len(text):
            new_list.append(TextNode(text[last_idx:], TextType.TEXT))

    return new_list

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
        last_idx = 0

        for link_text, url in matches:
            # Construct the full markdown image syntax

            markdown = f"[{link_text}]({url})"
            # Find position of this markdown in the remaining text
            start_idx = remaining_text.find(markdown)
            
            if start_idx == -1:

                continue
            
            # Add text before the image if any
            if start_idx > last_idx:
                result.append(TextNode(remaining_text[last_idx:start_idx], TextType.TEXT))
            
            # Add the link node
            result.append(TextNode(link_text, TextType.LINK, url))
            
            # Update remaining_text to be everything after the markdown
            last_idx = start_idx + len(markdown)

        # Add any remaining text
        if last_idx < len(remaining_text):
            result.append(TextNode(remaining_text[last_idx:], TextType.TEXT))
    
    return result
 

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    print(f"nodes after split_nodes_image: {nodes}")
    nodes = split_nodes_link(nodes)
    print(f"nodes after split_nodes_link: {nodes}")
    nodes = split_nodes_bold(nodes)
    print(f"nodes after split_nodes_blod: {nodes}")
    nodes = split_nodes_italic(nodes)
    print(f"nodes after split_nodes_italic: {nodes}")
    nodes = split_nodes_code(nodes)
    print(f"nodes after split_nodes_code: {nodes}")
    return nodes
