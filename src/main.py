import os
import shutil

from block_html import markdown_to_html_node
from blocks_md import HEADING, block_to_block_type, markdown_to_blocks

PUBLIC = "/Users/ja3faral-muallim/workspace/Learning/ssg/public"
STATIC = "/Users/ja3faral-muallim/workspace/Learning/ssg/static"
CONTENTS = "/Users/ja3faral-muallim/workspace/Learning/ssg/contents"
TEMPLATE = "/Users/ja3faral-muallim/workspace/Learning/ssg/template.html"


def main():
    status = delete_all_content(PUBLIC)
    if status:
        os.mkdir("public")
        copy_recursive(STATIC)
        # generate_page(contents, template, public)
        generate_pages_recursive(CONTENTS, TEMPLATE, PUBLIC)


def copy_recursive(path):
    if not os.path.exists(path):
        return
    all_path = path.split("/")
    dirname = all_path[len(all_path) - 2]
    if os.path.isfile(path):
        if dirname != "static":
            shutil.copy(path, os.path.join(PUBLIC, dirname))
        else:
            shutil.copy(path, PUBLIC)
        return
    files = os.listdir(path)
    dirname = all_path[len(all_path) - 1]
    if dirname != "static":
        os.mkdir(os.path.join(PUBLIC, dirname))
    for file in files:
        copy_recursive(os.path.join(path, file))


def delete_all_content(path):
    if not os.path.exists(path):
        return True
    shutil.rmtree(path)
    return True


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == HEADING and block.startswith("# "):
            return block.split("# ")[1]
    return " "


def generate_page(from_path, template_path, dest_path):
    file_name = from_path.split("/")[len(from_path.split("/")) - 1]
    file_name = file_name.replace(".md", ".html")
    with open(template_path) as template, open(from_path) as md, open(
        os.path.join(dest_path, file_name), mode="w"
    ) as new_doc:
        lines = template.read()
        md_lines = md.read()
        title = extract_title(md_lines)
        content = markdown_to_html_node(md_lines).to_html()
        lines = lines.replace("{{ Title }}", title).replace("{{ Content }}", content)
        new_doc.write(lines)
    return


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    all_path = dir_path_content.split("/")
    if os.path.isfile(dir_path_content):
        generate_page(dir_path_content, template_path, dest_dir_path)
        return

    files = os.listdir(dir_path_content)

    dirname = all_path[len(all_path) - 1]
    if dirname != "contents":
        os.mkdir(os.path.join(PUBLIC, dirname))
    for file in files:
        generate_pages_recursive(
            (
                os.path.join(CONTENTS, dirname, file)
                if dirname != "contents"
                else os.path.join(CONTENTS, file)
            ),
            template_path,
            os.path.join(PUBLIC, dirname) if dirname != "contents" else PUBLIC,
        )

    return

    # all_path = path.split("/")
    # dirname = all_path[len(all_path) - 2]
    # if os.path.isfile(path):
    #     if dirname != "static":
    #         shutil.copy(path, os.path.join(public, dirname))
    #     else:
    #         shutil.copy(path, public)
    #     return
    # dirname = all_path[len(all_path) - 1]
    # if dirname != "static":
    #     os.mkdir(os.path.join(public, dirname))
    # for file in files:
    #     copy_recursive(os.path.join(path, file))


main()
