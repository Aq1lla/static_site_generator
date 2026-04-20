import shutil
import os


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

    
