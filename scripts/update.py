from config import validate_and_get_docs_url, validate_and_get_selectors, find_project_root, load_config, CONFIG_PATH, README_PATH
from parse import build_layout_sections_string, normalize_layout_name, parse_directory_structure
from retrieve import fetch_directory_structures

from pathlib import Path
import argparse
import os
import re


def create_template_structure(base_path, structure, write_comments=True):
    """
    Recursively creates a directory structure at the specified base path according to the
    given structure.

    Args:
        base_path (str or Path): The base path where the directory structure starts.
        structure (list): The directory structure as a list of dictionaries.
        write_comments (bool, optional): Whether to write comments in files. Defaults to True.
    """
    # Convert base_path to a Path object if it's a string
    base_path = Path(base_path)

    # Create the base directory if it doesn't exist
    base_path.mkdir(parents=True, exist_ok=True)

    # Iterate through the structure to create directories and files
    for item in structure:
        current_path = base_path / item['path']
        if item['type'] == 'directory':
            # Create directory
            current_path.mkdir(parents=True, exist_ok=True)
            if 'children' in item:
                # Recursively create subdirectories/files
                create_template_structure(current_path, item['children'], write_comments=write_comments)
        elif item['type'] == 'file':
            # Create file
            with current_path.open('w') as file:
                # Optionally write the comment at the top of the file
                if write_comments and item['comment']:
                    file.write(f"# {item['comment']}\n")


def update_directory_structures(structures, base_path):
    """
    Processes each directory structure and creates corresponding templates.

    Args:
        structures (dict): A dictionary with layout names as keys and directory structure text as values.
        base_path (Path): The base path where the templates should be created.
    """
    for layout_name, structure_text in structures.items():
        normalized_name = normalize_layout_name(layout_name)
        parsed_structure = parse_directory_structure(structure_text)
        layout_base_path = base_path / 'templates' / normalized_name
        create_template_structure(layout_base_path, parsed_structure)
        print(f"Structure created for layout: {normalized_name}")


def update_readme_with_structure(structures, readme_path="README.md"):
    """
    Updates the README file with structured directory layouts in code blocks.

    Args:
        structures (dict): A dictionary with layout names as keys and directory structure text as values.
        readme_path (str): Path to the README file.
    """
    # Generate the combined layout sections string
    full_content = build_layout_sections_string(structures)

    # Read the current README content
    with open(readme_path, 'r', encoding='utf-8') as file:
        readme_content = file.read()

    # Define markers for where to insert the generated content
    start_marker = "<!-- TEMPLATE_START -->"
    end_marker = "<!-- TEMPLATE_END -->"

    # Replace content between markers
    updated_content = re.sub(f"{start_marker}.*?{end_marker}",
                             f"{start_marker}\n{full_content}\n{end_marker}",
                             readme_content,
                             flags=re.DOTALL)

    # Write the updated content back to the README
    with open(readme_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

    print("README updated with the latest directory structures.")


def main(force_updates=False):
    """
    Main function to orchestrate updates based on Ansible documentation.

    Args:
        force_updates (bool): Optionally forces updates without argparse flags.
    """
    parser = argparse.ArgumentParser(
        description='Automatically updates Ansible template structures and README based on the latest documentation.')

    # Define command-line arguments for optional actions
    parser.add_argument('--update-readme',
                        action='store_true',
                        help='Optionally update README.md with the latest structure changes.')
    parser.add_argument('--update-directories',
                        action='store_true',
                        help='Optionally update directory structures to reflect current Ansible documentation.')

    args = parser.parse_args()

    # Configuration loading
    config = load_config(CONFIG_PATH)
    """Loads configuration settings from a specified path."""

    # Directory structures fetching
    docs_url = validate_and_get_docs_url(config)
    selectors = validate_and_get_selectors(config)
    structures = fetch_directory_structures(docs_url, selectors)
    """Retrieves and parses directory structures from Ansible documentation."""

    # Base path determination
    script_dir = Path(__file__).resolve().parent
    project_root = find_project_root(script_dir)
    base_path = Path(os.getenv('GITHUB_WORKSPACE', project_root))
    """Determines the base path for updates, accommodating local and CI environments."""

    # README.md update
    if args.update_readme or force_updates:
        update_readme_with_structure(structures, README_PATH)
        """Updates the README.md file with the latest directory structures if flagged."""

    # Template directories update
    if args.update_directories or force_updates:
        update_directory_structures(structures, base_path)
        """Updates the template directories to match the latest Ansible documentation structures if flagged."""


if __name__ == "__main__":
    main()
