from bs4 import BeautifulSoup
import requests


def fetch_directory_structures(docs_url: str, selectors: list) -> dict:
    """
    Fetches directory structures from a webpage.

    Args:
        docs_url (str): The URL of the webpage.
        selectors (list): List of selectors to search for.

    Returns:
        dict: Dictionary containing directory structures for each selector.
    """
    # Fetch webpage content
    response = requests.get(docs_url)

    # Check if the request was successful
    if response.status_code != 200:
        raise ConnectionError(f"Failed to fetch the webpage, status code: {response.status_code}")

    # Parse HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    structures = {}

    # Extract directory structures for each selector
    for selector in selectors:
        section = soup.find(id=selector)
        if section:
            # Find all code blocks within the section
            code_blocks = section.find_all('div', class_='highlight')
            # Concatenate text from all <pre> tags within code blocks
            structure_text = '\n'.join(pre.get_text() for block in code_blocks for pre in block.find_all('pre'))
            structures[selector] = structure_text
        else:
            print(f"No section found for selector: {selector}")
            structures[selector] = ""

    return structures


if __name__ == "__main__":
    import configparser

    # Load configuration from config.ini
    config_parser = configparser.ConfigParser()
    config_parser.read('../config.ini')

    # Retrieve configuration variables
    docs_url_param = config_parser['DEFAULT']['DOCS_URL']
    selectors_param = [selector.strip() for selector in config_parser['DEFAULT']['SELECTORS'].split(',')]

    # Fetch directory structures
    structures_retrieved = fetch_directory_structures(docs_url_param, selectors_param)

    # Display retrieved structures
    for selector, structure in structures_retrieved.items():
        if structure:
            print(f"\nStructure for {selector}:\n{structure}\n")
        else:
            print(f"No structure found for {selector}.")
