from textnode import *
from main_functions import *


def main():
    init_page("./static", "./public")
    generate_pages_recursive("./content", "template.html", "./public")

main()