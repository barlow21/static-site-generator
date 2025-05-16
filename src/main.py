import os
from pathlib import Path
import re
import shutil
import sys
from markdown_blocks import extract_title, markdown_to_html_node


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
    try:
        shutil.rmtree(public_dir)
    except FileNotFoundError:
        pass
    os.mkdir(public_dir)
    copy_directory(static_dir, public_dir)


def generate_page(from_path, dest_path, template_path, basepath):
    markdown = Path(from_path).read_text()
    output = Path(template_path).read_text()
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    output = re.sub(r".*\{\{ Title \}\}.*", title, output)
    output = re.sub(r".*\{\{ Content \}\}.*", content, output)
    output = re.sub(r'href="/', f'href="{basepath}', output)
    output = re.sub(r'src="/', f'src="{basepath}', output)

    Path(dest_path).write_text(output)


def generate_pages(src, dest, template_path, basepath):
    for name in os.listdir(src):
        fullname = os.path.join(src, name)
        dest_name = os.path.join(dest, name)
        if os.path.isfile(fullname):
            generate_page(
                fullname, dest_name.replace(".md", ".html"), template_path, basepath
            )
        else:
            os.mkdir(dest_name)
            generate_pages(fullname, dest_name, template_path, basepath)


def main():
    basepath = "/"
    print(len(sys.argv))
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    cwd = os.getcwd()
    static_dir = os.path.join(cwd, "static")
    docs_dir = os.path.join(cwd, "docs")
    copy_static_content(static_dir, docs_dir)

    content_dir = os.path.join(cwd, "content")
    template_path = os.path.join(cwd, "template.html")
    generate_pages(content_dir, docs_dir, template_path, basepath)


main()
