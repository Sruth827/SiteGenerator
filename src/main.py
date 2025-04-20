import os
import shutil 

from textnode import *
from utils import generate_pages_recursive


def recursive_file_copy(destination_dir, source_dir):
    destination_dir = os.path.expanduser(destination_dir)
    source_dir = os.path.expanduser(source_dir)

    if os.path.exists(destination_dir):
        print(f"rmtree of destination dir")
        shutil.rmtree(destination_dir)
    print(f"creating a new destination dir")
    os.mkdir(destination_dir)

    #gets all items in source dir
    source_items = os.listdir(source_dir)

    for item in source_items:
        #this gets full path for destination and source
        source_item_path = os.path.join(source_dir, item)
        destination_item_path = os.path.join(destination_dir, item)

        if os.path.isfile(source_item_path):
            print(f"copying file: {source_item_path} to {destination_item_path}")
            shutil.copy(source_item_path, destination_item_path)

        if os.path.isdir(source_item_path):
            print(f"copying directory: {source_item_path} to {destination_item_path}")
            #recursive call to copy subdirectory
            recursive_file_copy(destination_item_path, source_item_path)



def main(): 
    newnode = TextNode("this is some anchor text", TextType.LINK, "https://www.sean.com/")
    print(newnode)
    

    source = os.path.expanduser("~/SiteGenerator/static")
    destination = os.path.expanduser("~/SiteGenerator/public")
    template = os.path.expanduser("~/SiteGenerator/template.html")
    content = os.path.expanduser("~/SiteGenerator/content")
    recursive_file_copy(destination, source)
    generate_pages_recursive(content, template, destination) 

if __name__ == "__main__":
    main()

