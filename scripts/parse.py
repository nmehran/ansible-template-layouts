def parse_directory_structure(directory_structure):
    """
    Parses the directory structure string into a structured format.

    :param directory_structure: The directory structure as a string.
    :return: A list of dictionaries representing the directory structure.
    """
    lines = directory_structure.split('\n')
    tree = []
    path_stack = []  # To keep track of current path based on indentation

    for line in lines:
        if not line.strip():
            continue  # Skip empty lines

        # Determine the level of indentation (assuming 4 spaces per level)
        level = (len(line) - len(line.lstrip())) // 4

        # Extract the path and optional comment
        parts = line.strip().split('#', 1)
        path = parts[0].strip()
        comment = parts[1].strip() if len(parts) > 1 else ""

        # Adjust the path stack based on the current level of indentation
        path_stack = path_stack[:level]
        path_stack.append(path)

        # Create a structured entry for this line
        entry = {
            "type": "file" if "." in path else "dir",
            "path": "/".join(path_stack),
            "comment": comment
        }

        tree.append(entry)

    return tree
