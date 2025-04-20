import re 
import os
from splitblock import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.splitlines()  # Split into individual lines
    for line in lines:
        if line.startswith("# "):  # Check for `#` followed by a space
            title = line[2:].strip()  # Remove the `# ` and strip extra spaces
            print(f"Extracted title: {title}")
            return title
    raise Exception("No title (h1) found in the markdown!")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
     for root, dirs, files in os.walk(dir_path_content):
        relative_path = os.path.relpath(root, dir_path_content)
        destination_dir = os.path.join(dest_dir_path, relative_path)
        os.makedirs(destination_dir, exist_ok=True)
        
        for file in files:
            if file.endswith('.md'):     
                source_file = os.path.join(root, file)
                destination_file_name = file.replace('.md', '.html')
                destination_file = os.path.join(destination_dir, destination_file_name)
                generate_page(source_file, template_path, destination_file)
        

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_text = ""
    template_text = ""

    #read markdown file store in markdown_text 
    if os.path.exists(from_path):
        with open(from_path) as f:
            markdown_text = f.read()
    else: 
        raise FileNotFoundError(f"Markdown File not found at {from_path}")
    print(f"Markdown content loaded: {markdown_text[:50]}")

    #read the template store in template_text
    if os.path.exists(template_path):
        with open(template_path) as f:
            template_text = f.read()
    else: 
        raise FileNotFoundError(f"Template File not found at {tempate_path}")
    print(f"Template content loaded: {template_text[:100]}")

    #convert markdown to HTML format
    html_string = markdown_to_html_node(markdown_text).to_html()
    #extract the title from markdown
    try:
        title = extract_title(markdown_text)
    except Exception as e:
        raise Exception(f"Failure to extract title: {e}")
    print(f"Title extracted: {title}")

    #use title and hmtl format to replace placeholders
    generated_page = template_text.replace("{{ Title }}", title)
    html_page = generated_page.replace("{{ Content }}", html_string)
    print(f"Final HTML Page:\n{html_string}")

    #make dir if not created, if exists use dir, write to dir using generated page
    os.makedirs(os.path.dirname(dest_path), exist_ok=True) 
    with open(dest_path, "w") as output_file:
        output_file.write(html_page)

