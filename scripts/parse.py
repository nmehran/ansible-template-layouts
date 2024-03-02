from retrieve import fetch_directory_structures


def parse_structure(structure_text):
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
    structures = fetch_directory_structures()
    # Parsing the sample-directory-layout
    parsed_sample_layout = parse_structure(structures['sample-directory-layout'])
    print(parsed_sample_layout)
    #
    # # Parsing the alternative-directory-layout
    # parsed_alternative_layout = parse_structure(structures['alternative-directory-layout'])
    # print(parsed_alternative_layout)
