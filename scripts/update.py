from config import validate_and_get_docs_url, validate_and_get_selectors, find_project_root, load_config
from parse import build_structure_string, normalize_layout_name, parse_directory_structure
from retrieve import fetch_directory_structures

from pathlib import Path
import os


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


def main():
    # Load configuration using the optimized load_config function
    config = load_config('../config.ini')

    # Validate and retrieve necessary configuration values
    docs_url = validate_and_get_docs_url(config)
    selectors = validate_and_get_selectors(config)

    # Fetch directory structures
    structures = fetch_directory_structures(docs_url, selectors)

    # Determine the script directory assuming it's run from within the 'scripts' directory
    script_dir = Path(__file__).resolve().parent
    project_root = find_project_root(script_dir)

    # Determine base path using GITHUB_WORKSPACE if available, or default to project root
    base_path = Path(os.getenv('GITHUB_WORKSPACE', project_root))

    # Process each directory structure
    for layout_name, structure_text in structures.items():
        normalized_name = normalize_layout_name(layout_name)
        parsed_structure = parse_directory_structure(structure_text)
        layout_base_path = base_path / 'templates' / normalized_name
        create_template_structure(layout_base_path, parsed_structure)
        print(f"Structure created for layout: {layout_name}")


if __name__ == "__main__":
    main()
