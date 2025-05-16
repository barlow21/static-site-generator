import os
from pathlib import Path
import re
import shutil
from markdown_blocks import extract_title, markdown_to_html_node
from textnode import TextNode, TextType


def copy_directory(src, dest):
    for name in os.listdir(src):
        fullname = os.path.join(src, name)
        if os.path.isfile(fullname):
            shutil.copy(fullname, dest)

        else:
            new_dir = os.path.join(dest, name)
            os.mkdir(new_dir)
            copy_directory(fullname, new_dir)


def copy_static_content(static_dir, public_dir):
    shutil.rmtree(public_dir)
    os.mkdir(public_dir)
    copy_directory(static_dir, public_dir)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown = Path(from_path).read_text()
    output = Path(template_path).read_text()
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    output = re.sub(r".*\{\{ Title \}\}.*", title, output)
    output = re.sub(r".*\{\{ Content \}\}.*", content, output)

    Path(dest_path).write_text(output)


def main():
    cwd = os.getcwd()
    static_dir = os.path.join(cwd, "static")
    public_dir = os.path.join(cwd, "public")
    copy_static_content(static_dir, public_dir)

    index_md = os.path.join(cwd, "content", "index.md")
    target = os.path.join(public_dir, "index.html")
    template = os.path.join(cwd, "template.html")
    generate_page(index_md, template, target)


main()
