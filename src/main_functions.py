import shutil
import os

from functions import markdown_to_html_node


def init_page(src, dest):
    """
    Function that copies all the contents from a source directory to a destination directory (in our case, static to public)
    """

    # 1.- delete all the contents of the destination directory (public) to ensure that the copy is clean
    if os.path.exists(dest):
        shutil.rmtree(dest)

    # 2.- create destination folder
    os.mkdir(dest)

    # 3.- Get src content
    dir_content = os.listdir(src)

    for item in dir_content:
        item_path = os.path.join(src, item)
        
        # If it is file, copy
        if os.path.isfile(item_path):
            shutil.copy(item_path, dest)
            # 4.- logging the path of each file you copy, so you can see what's happening as you run and debug your code
            print(f"Copied file: {item_path} -> {os.path.join(dest, item)}")
        
        # Else, make directory and recurse
        else:
            dir_path = os.path.join(dest, item)
            os.mkdir(dir_path)
            init_page(item_path, dir_path)


def extract_title(markdown):
    content = markdown.split("\n")

    for item in content:
        if item.startswith("#"):
            return item[1:].strip()
    
    raise Exception("No header")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path) as f:
        content = f.read()
    f.close()

    with open(template_path) as f:
        template = f.read()
    f.close()

    content_string = markdown_to_html_node(content)
    title = extract_title(content)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content_string.to_html())

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w') as f:
        f.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Function that: 
        - Crawls every entry in the content directory
        - For each markdown file found, generate a new .html file using the same template.html. The generated pages 
        should be written to the public directory in the same directory structure.
    """
    if not os.path.isfile(dir_path_content):
        dir_content = os.listdir(dir_path_content)

        for item in dir_content:      
            item_path = os.path.join(dir_path_content, item)

            # If it is file, copy
            if os.path.isfile(item_path) and item_path.endswith('.md'):
                dest_path = os.path.join(dest_dir_path, item.replace('.md', '.html'))
                generate_page(item_path, template_path, dest_path)
            
            # Else, make directory and recurse
            else:
                dest_subdir = os.path.join(dest_dir_path, item)
                os.makedirs(dest_subdir, exist_ok=True)
                generate_pages_recursive(item_path, template_path, dest_subdir)