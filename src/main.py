from textnode import *
from main_functions import *
import sys


def main():
    basepath = "/" if len(sys.argv) < 2 or sys.argv[1] == "" else sys.argv[1]

    init_page("./static", "./docs")
    generate_pages_recursive("./content", "template.html", "./docs", basepath)

main()