from retrieve import fetch_directory_structures


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
    lines = structure_text.split('\n')  # Split the input text into individual lines.
    analyzed_lines = []  # Initialize a list to keep track of analyzed lines.

    # Process each line to determine if it's a directory or a file.
    for line in lines:
        # Skip over empty lines or lines that start with a comment.
        if not line.strip() or '#' in line.strip().split()[0]:
            continue

        # Calculate the indentation level of the current line.
        indent_level = len(line) - len(line.lstrip())

        # Determine if the line represents a directory or a file.
        is_directory = line.strip().endswith('/')
        is_file = not is_directory and not line.strip().split()[0].startswith('#')

        # Add directories and files to the analyzed lines list with their indentation levels.
        if is_directory or is_file:
            analyzed_lines.append((indent_level, line.strip()))

    # Determine the common indentation difference by analyzing the indentation changes between lines.
    indent_differences = [current_indent - previous_indent for previous_indent, current_indent in
                          zip([0] + [lvl for lvl, _ in analyzed_lines[:-1]], [lvl for lvl, _ in analyzed_lines])]
    indent_differences = [diff for diff in indent_differences if diff > 0]  # Keep only positive differences.

    # Calculate the most common indentation difference; default to 4 if none is found.
    common_indent = max(indent_differences, key=indent_differences.count) if indent_differences else 4

    return common_indent, analyzed_lines


def parse_directory_structure(directory_text):
    """
    Parses the directory structure from a given text using a determined common indentation
    to accurately structure the hierarchy. This function adjusts indentation levels to the nearest
    common indentation multiple, ensuring correct hierarchical representation.

    Args:
    - directory_text (str): The directory structure as a multiline string.

    Returns:
    - dict: A nested dictionary representing the directory structure, with each node containing
      the type (file or directory), path, comment (if any), and children (a list of nested nodes).
    """
    common_indent, analyzed_lines = analyze_structure(directory_text)

    # Initialize the root of the directory structure.
    root = {'type': 'directory', 'path': 'root', 'comment': '', 'children': []}
    path_stack = [root]  # Use a stack to keep track of the current path context.

    for indent_level, line in analyzed_lines:
        # Split the line into path and optional comment.
        parts = line.split('#', 1)
        path = parts[0].strip()
        comment = parts[1].strip() if len(parts) > 1 else ''

        # Determine the item type and prepare the item dictionary.
        item = {'type': 'file' if '.' in path or not path.endswith('/') else 'directory',
                'path': path, 'comment': comment, 'children': []}

        # Adjust the indent level to the closest multiple of the common indentation.
        lower_multiple = (indent_level // common_indent) * common_indent
        upper_multiple = lower_multiple + common_indent
        adjusted_indent_level = lower_multiple if (indent_level - lower_multiple) < (
                    upper_multiple - indent_level) else upper_multiple

        # Determine the current level in the hierarchy based on adjusted indentation.
        current_level = adjusted_indent_level // common_indent
        path_stack = path_stack[:current_level + 1]  # Adjust the path stack to the current context.
        parent = path_stack[-1]  # Identify the current parent node.

        # Append the current item to the parent's children and update the path stack if necessary.
        parent['children'].append(item)
        if item['type'] == 'directory':
            path_stack.append(item)  # Directories can have children, so add them to the path stack.

    return root['children']



def print_structure(structure, indent=0, comment_indent=30):
    """
    Recursively prints the directory structure with aligned comments.

    Args:
        structure (list): List of nested dictionaries representing the directory structure.
        indent (int): Current indentation level for this print call.
        comment_indent (int): Column position to align comments.
    """
    for item in structure:
        base_line = f"{' ' * indent}{'📁' if item['type'] == 'directory' else '📄'} {item['path']}"
        # Ensure comments are aligned uniformly
        comment_str = f" # {item['comment']}" if item['comment'] else ""
        # Calculate padding for alignment
        padding = max(comment_indent - len(base_line), 1)
        print(f"{base_line}{' ' * padding}{comment_str}")
        if item['children']:
            print_structure(item['children'], indent + 4, comment_indent)


if __name__ == "__main__":
    import configparser

    # Load configuration
    config = configparser.ConfigParser()
    config.read('../config.ini')

    # Configuration variables
    docs_url = config['DEFAULT']['DOCS_URL']
    selectors = [selector.strip() for selector in config['DEFAULT']['SELECTORS'].split(',')]

    # Fetch directory structures
    structures = fetch_directory_structures(docs_url, selectors)

    # Parsing the sample-directory-layout

    # Test the new function with the structure text
    structure_text = structures['sample-directory-layout']

    print_structure(parse_directory_structure(structure_text))

    # Uncomment below to parse additional directory layouts
    # Parsing the alternative-directory-layout
    # parsed_alternative_layout = parse_structure(structures['alternative-directory-layout'])
    # print(parsed_alternative_layout)
