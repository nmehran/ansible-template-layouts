from retrieve import fetch_directory_structures
import configparser


def analyze_structure(structure_text):
    """
    Analyzes the provided directory structure text to identify and record the indentation level
    and content of each line that represents a file or directory. It skips over empty lines and
    comments, focusing on structural elements only.

    Args:
    - structure_text (str): The directory structure as a multiline string.

    Returns:
    - tuple: A tuple containing the most common indentation difference (int) and a list of tuples,
      each with the indentation level (int) and the content (str) of the line.
    """
    # Strip leading/trailing whitespace and split the text into lines for processing
    lines = structure_text.strip().split('\n')
    analyzed_lines = []  # List to hold tuples of (indentation level, line content)
    indent_differences = []  # List to track differences in indentation between hierarchy levels

    previous_indent_level = 0  # Initialize previous indentation level for comparison

    for line in lines:
        stripped_line = line.strip()
        # Skip empty lines or lines that start with a '#' (comments)
        if not stripped_line or stripped_line.startswith('#'):
            continue

        # Calculate the current line's indentation level
        indent_level = len(line) - len(stripped_line)

        # If the current indentation is greater than the previous, record the difference
        if indent_level > previous_indent_level:
            indent_differences.append(indent_level - previous_indent_level)

        # Update the previous indentation level for the next iteration
        previous_indent_level = indent_level

        # Append the current line's indentation level and stripped content to the analyzed lines
        analyzed_lines.append((indent_level, stripped_line))

    # Determine the most common indentation difference; default to 4 if no difference is found
    common_indent = max(set(indent_differences), key=indent_differences.count, default=4)

    return common_indent, analyzed_lines


def parse_directory_structure(directory_text):
    """
    Parses a given directory structure text into a nested dictionary representing the hierarchical
    structure of directories and files. It uses a common indentation level to accurately determine
    the hierarchy, adjusting indentation levels to the nearest common indentation multiple.

    Args:
        directory_text (str): Multiline string representation of a directory structure.

    Returns:
        list: A list of nested dictionaries. The root directory is represented as a list containing
              a single dictionary that may contain children dictionaries for subdirectories and files.
              Each dictionary has keys for type (file or directory), path, optional comment, and
              children (for directories).
    """
    # Analyze the structure to get common indentation and list of lines with their indentation levels.
    common_indent, analyzed_lines = analyze_structure(directory_text)

    root = {'type': 'directory', 'path': '/', 'comment': '', 'children': []}
    path_stack = [root]  # Stack to track the current path context.

    for indent_level, line in analyzed_lines:
        parts = line.split('#', 1)
        path = parts[0].strip()
        comment = parts[1].strip() if len(parts) > 1 else ''

        item = {
            'type': 'directory' if path.endswith('/') else 'file',
            'path': path.rstrip('/'),  # Ensure directory paths do not end with a slash
            'comment': comment,
            'children': [] if path.endswith('/') else None  # Files do not have children
        }

        # Adjust indentation level to the nearest multiple of common indentation.
        adjusted_level = round(indent_level / common_indent) * common_indent

        # Find parent based on adjusted indentation level.
        while len(path_stack) > adjusted_level // common_indent + 1:
            path_stack.pop()

        # Append the item to its parent's children and update the path stack for directories.
        path_stack[-1]['children'].append(item)
        if item['type'] == 'directory':
            path_stack.append(item)

    return root['children']


def build_structure_string(structure, indent=0, comment_indent=30):
    """
    Recursively builds a string representation of the directory structure with aligned comments,
    ensuring that comments are aligned at a specified column position. This function uses recursion
    to handle nested directories and files, returning the entire structure as a single string.

    Args:
        structure (list): List of nested dictionaries representing the directory structure.
        indent (int): Current indentation level for this call.
        comment_indent (int): Column position to align comments.

    Returns:
        str: A single string representation of the directory structure with aligned comments.
    """
    lines = []  # Collect lines here
    icon_mapping = {'directory': '📁', 'file': '📄'}  # Icons for directory and file.

    for item in structure:
        # Construct the base line with the appropriate icon and path.
        icon = icon_mapping.get(item['type'], '❓')  # Default to '❓' for unknown types.
        base_line = f"{' ' * indent}{icon} {item['path']}"

        # Prepare the comment string, if any, with alignment.
        comment_str = f" # {item['comment']}" if item['comment'] else ""
        padding = max(comment_indent - len(base_line), 1)  # Ensure at least one space before the comment.

        line = f"{base_line}{' ' * padding}{comment_str}"
        lines.append(line)

        if item.get('children'):
            # Recursively build the string for children, increasing the indentation.
            child_str = build_structure_string(item['children'], indent + 4, comment_indent)
            lines.append(child_str)

    return '\n'.join(lines)  # Join all lines into a single string.


def main():
    # Load configuration
    config = configparser.ConfigParser()
    config.read('../config.ini')

    # Extract configuration variables.
    docs_url = config['DEFAULT']['DOCS_URL']
    selectors = [selector.strip() for selector in config['DEFAULT']['SELECTORS'].split(',')]

    # Fetch directory structures based on the provided URL and selectors.
    structures = fetch_directory_structures(docs_url, selectors)

    # Assuming fetch_directory_structures returns a dict with keys being layout names
    # and values being the directory structure text.
    for layout_name, structure_text in structures.items():
        print(f"'{layout_name}':")
        parsed_structure = parse_directory_structure(structure_text)
        print(build_structure_string(parsed_structure))
        print("\n---\n")  # Separator between different directory layouts.


if __name__ == "__main__":
    main()
