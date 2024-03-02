from retrieve import fetch_directory_structures


def parse_structure(structure_text) -> list:
    """
    Parse directory structure text into a list of dictionaries.

    Args:
        structure_text (str): The directory structure text.

    Returns:
        list: List of dictionaries, each representing a directory or file.
    """
    structure_lines = structure_text.strip().split('\n')
    parsed_structure = []

    for line in structure_lines:
        if not line.strip():
            continue  # Skip empty lines

        # Split line into path and comment
        parts = line.split('#', 1)
        path = parts[0].strip()
        comment = parts[1].strip() if len(parts) > 1 else ""

        # Determine if the current line represents a directory or a file
        if path.endswith('/'):
            item_type = 'directory'
            path = path[:-1]  # Remove trailing slash for consistency
        else:
            item_type = 'file'

        parsed_structure.append({
            'type': item_type,
            'path': path,
            'comment': comment
        })

    return parsed_structure


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
    parsed_sample_layout = parse_structure(structures['sample-directory-layout'])
    print(parsed_sample_layout)

    # Uncomment below to parse additional directory layouts
    # Parsing the alternative-directory-layout
    # parsed_alternative_layout = parse_structure(structures['alternative-directory-layout'])
    # print(parsed_alternative_layout)
