"""
Service for organizing process of creating flashcards from notes.
"""
import datetime
import os
from collections import OrderedDict
from typing import TextIO

NOTES_ROOT = r"..\Notes"
CHECKLIST_FILE = r"..\Flashcards_checklist.md"


def get_notes_files_dict(root_dir: str) -> dict:
    """
    Returns dict containing data about all Markdown files in NOTES_ROOT directory.

    Args:
        root_dir (str): Root directory

    Returns:
        dict: Dict containing all .md files stored in given root dir.
    """
    return_dict = OrderedDict()
    for root, dirs, files in os.walk(root_dir):
        cleaned_root = root.replace(NOTES_ROOT + '\\', '')
        notes = {os.path.join(cleaned_root, file): False for file in files if file.endswith('.md')}
        if notes:
            return_dict[cleaned_root] = notes
    return return_dict


def get_checklist_files_dict(checklist_file: str) -> dict:
    """
    Returns dict containing data about all Markdown files mentioned in CHECKLIST_FILE.

    Args:
        checklist_file (str): Checklist file.

    Returns:
        dict: Dict containing all .md files mentioned in given checklist_file.
    """
    return_dict = OrderedDict()
    with open(checklist_file, mode='r') as file:
        sub_dir = None
        for line in file:
            line = line.strip()
            if line.startswith('##'):
                sub_dir = line.replace('##', '').strip()
                return_dict[sub_dir] = {}
            elif line.startswith('- [X]'):
                filename = line.replace('- [X]', '').replace('~~', '').strip()
                return_dict[sub_dir][filename] = True
            elif line.startswith('- [ ]'):
                filename = line.replace('- [ ]', '').strip()
                return_dict[sub_dir][filename] = False
    return return_dict


def get_final_dict(notes_dict: dict, checklist_dict: dict) -> dict:
    """
    Returns dict containing data collected from NOTES_ROOT then updated with data added in CHECKLIST_FILE.

    Args:
        notes_dict (dict): Dict containing all .md files stored in given root dir.
        checklist_dict (dict): Dict containing all .md files mentioned in given checklist_file.

    Returns:
        dict: Dict containing data collected from NOTES_ROOT then updated with data added in CHECKLIST_FILE.
    """
    final_dict = notes_dict.copy()
    for subdir in final_dict:
        if checklist_subdir := checklist_dict.get(subdir):
            final_dict[subdir].update(checklist_subdir)
    return final_dict


def write_content(file: TextIO, content: dict) -> None:
    """
    Writes given content dict to file.

    Args:
        file (TextIO): File instance.
        content (dict): File content.
    """
    file.write("# Flashcard checklist")
    for notes_subdir in content:
        file.write(f"\n## {notes_subdir}\n")
        subdir_files = content[notes_subdir]
        for notes_file in subdir_files:
            flashcards_done = subdir_files[notes_file]
            if flashcards_done:
                file.write(f'- [X] ~~{notes_file}~~\n')
            else:
                file.write(f'- [ ] {notes_file}\n')


def main(notes_dir: str, existing_checklist: str) -> None:
    """
    Executes whole process of:
    * Collecting .md notes files dict from source notes directory
    * Collecting .md notes files dict from existing checklist file
    * Creating new checklist file basing on source notes directory updated with data from existing checklist file.

    Args:
        notes_dir (str): Path to .md notes directory
        existing_checklist (str): Path to flashcards checklist file
    """
    notes_files_dict = get_notes_files_dict(root_dir=notes_dir)
    existing_checklist_files_dict = get_checklist_files_dict(existing_checklist)
    final_dict = get_final_dict(notes_dict=notes_files_dict, checklist_dict=existing_checklist_files_dict)
    notes_files_dict.update(existing_checklist_files_dict)
    with open(f'Checklists/Flashcards_checklist_{datetime.date.today()}.md', mode='w', encoding="utf8") as output_file:
        write_content(file=output_file, content=final_dict)


if __name__ == '__main__':
    main(notes_dir=NOTES_ROOT, existing_checklist=CHECKLIST_FILE)
