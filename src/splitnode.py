
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
    for match in re.finditer(r"_(.*?)_", text):
        matches.append((match.group(1), match.start(), match.end()))
    return matches

def extract_markdown_code(text):
    matches = []
    for match in re.finditer(r"`(.*?)`", text):
        matches.append((match.group(1), match.start(), match.end()))
    return matches 

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)



def split_nodes_image(old_nodes):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        matches = extract_markdown_images(node.text)
        if not matches:
            new_list.append(node)
            continue

        text = node.text
        for image_alt, image_link in matches:
            sections = text.split(f"![{image_alt}]({image_link})", 1)
            new_list.append(TextNode(sections[0], TextType.TEXT))
            new_list.append(TextNode(f"{image_alt}", TextType.IMAGE, f"{image_link}"))
            text = sections[1] if len(sections) > 1 else ""

        if text:
            new_list.append(TextNode(text, TextType.TEXT))
                        
    return new_list


def split_nodes_link(old_nodes):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        matches = extract_markdown_links(node.text)
        if not matches:
            new_list.append(node)
            continue

        text = node.text
        for link_alt, link in matches:
            sections = text.split(f"[{link_alt}]({link})", 1)
            new_list.append(TextNode(sections[0], TextType.TEXT))
            new_list.append(TextNode(f"{link_alt}", TextType.LINK, f"{link}"))
            text = sections[1] if len(sections) > 1 else ""

        if text:
            new_list.append(TextNode(text, TextType.TEXT))

    return new_list

def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]

    #Iterate over the extractor funcs to process the text type
    for extractor, delimiter, text_type in[
        (extract_markdown_bold, "**", TextType.BOLD),
        (extract_markdown_italic, "_", TextType.ITALIC),        
        (extract_markdown_code, "`", TextType.CODE)
        ]:

        temp_nodes = []
        for node in new_nodes:
            #if TEXT use the extractor to find any matches
            if node.text_type == TextType.TEXT:
                matches = extractor(node.text)
                if matches:
                    #split text of node into style parts
                    temp_nodes.extend(split_node_delimiter([node], delimiter, text_type))     
                else:
                    temp_nodes.append(node)
            else:
                #keep non-text nodes unchanged
                temp_nodes.append(node)
        new_nodes = temp_nodes
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_image(new_nodes)
    return new_nodes        
