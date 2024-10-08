import os
import re
import urllib.request
from urllib.parse import urljoin
from pathlib import Path
from typing import TextIO

NOTES_ROOT = r"..\Notes\\"
REPOSITORY_ROOT = "https://raw.githubusercontent.com/MateDawid/Learning/main/Notes/"


def get_table_of_content(searched_dir: str, input_dict: dict, excluded_dirs: list | None = None, ) -> dict:
    """
    Replicates given dir structure in form of dict.

    Args:
        searched_dir (str): Directory where structure is replicated.
        input_dict (dict): Dict to be enhanced with replicated structure.
        excluded_dirs (list|None): [Optional] List of directories excluded from replicating.

    Returns:
        dict: Dictionary with replicated Notes dir structure
    """

    for root, dirs, files in os.walk(searched_dir):
        if not [subdir for subdir in dirs if subdir not in excluded_dirs]:
            for file in files:
                input_dict[file] = os.path.join(root, file)
            return input_dict
        for dir_name in dirs:
            if excluded_dirs and dir_name in excluded_dirs:
                continue
            dir_path = os.path.join(root, dir_name)
            dir_key = dir_path.replace(NOTES_ROOT, '')
            input_dict[dir_key] = dict()
            get_table_of_content(searched_dir=dir_path, input_dict=input_dict[dir_key], excluded_dirs=excluded_dirs)
        break  # Exits os.walk after highest root encountered
    return input_dict


def get_fixed_image_line(line: str, line_images: list, header_file: str):
    for alt, filename, resize in line_images:
        if filename.startswith("http"):
            continue
        else:
            images_dir_path = os.path.dirname(header_file)
            fixed_filename = Path(images_dir_path, filename)
            if not os.path.exists(fixed_filename):
                raise Exception(f'get_fixed_image_line: Path {fixed_filename} does not exist!')
            images_dir_url = urljoin(
                REPOSITORY_ROOT,
                urllib.request.pathname2url(
                    images_dir_path.replace(NOTES_ROOT, '')
                )
            ) + '/'
            file_url = urljoin(images_dir_url, filename)
        if resize:
            resize = resize.strip()
            line = line.replace(f"![{alt}]({filename} {resize})", f"![{alt}]({file_url} {resize})")
        else:
            line = line.replace(f"![{alt}]({filename})", f"![{alt}]({file_url})")

    return line


def write_content(file: TextIO, content_dict: dict, depth: int) -> None:
    def add_new_header():
        if depth == 0:
            file.write(f'{header}\n{len(header) * "="}\n\n')
        write_content(file=file, content_dict=header_content, depth=depth + 1)

    def add_new_content():
        file.write(f'# {header_content.replace(NOTES_ROOT, "")}\n\n')
        with open(header_content, mode='r', encoding="utf8") as content_file:
            for line in content_file.readlines():
                if line.startswith('#'):
                    file.write(f'{"#" * (depth - 1)}{line}')
                elif images := re.findall(r"!\[([^]]*)\]\(([^\s]+)(\s\".*\")*\)", line):
                    file.write(get_fixed_image_line(line=line, line_images=images, header_file=header_content))
                else:
                    file.write(line)
            file.write('\n')

    for header, header_content in content_dict.items():
        if isinstance(header_content, dict):
            add_new_header()
        elif isinstance(header_content, str):
            add_new_content()


if __name__ == '__main__':

    table_of_content = get_table_of_content(searched_dir=NOTES_ROOT, input_dict={}, excluded_dirs=['_images'])
    with open('MergedNotes.md', mode='w', encoding="utf8") as output_file:
        write_content(file=output_file, content_dict=table_of_content, depth=0)
