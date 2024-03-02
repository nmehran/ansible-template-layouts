from config import validate_and_get_docs_url, validate_and_get_selectors, load_config, CONFIG_PATH
from bs4 import BeautifulSoup
import requests


def fetch_directory_structures(docs_url: str, selectors: list) -> dict:
    """
    Fetches directory structures from a webpage, handling both CSS selectors and element IDs.
    This function requests the webpage content, parses it, and then searches for specified
    selectors to extract directory structures, typically contained within <pre> tags.

    Args:
        docs_url (str): The URL of the webpage from which to fetch directory structures.
        selectors (list): A list of CSS selectors or element IDs to identify the sections
                          containing the directory structures.

    Returns:
        dict: A dictionary mapping each selector to its corresponding directory structure text.
              If no content is found for a selector, it maps to an empty string.

    Raises:
        ConnectionError: If the HTTP request to fetch the webpage fails or returns a non-200 status code.
        ValueError: If the provided selectors list is empty.
    """
    # Validate input
    if not selectors:
        raise ValueError("Selectors list cannot be empty.")

    try:
        response = requests.get(docs_url)
        response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx, 5xx)
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Failed to fetch the webpage: {e}")

    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, 'html.parser')
    structures = {}

    for selector in selectors:
        # Handle both CSS selectors and element IDs with a unified approach
        section = soup.select_one(f'#{selector}' if str(selector[0]).isalnum() else selector)
        if section:
            # Assuming directory structures are within <pre> tags
            structure_text = '\n'.join(pre.get_text() for pre in section.find_all('pre'))
            structures[selector] = structure_text.strip()
        else:
            print(f"No content found for selector: '{selector}'.")
            structures[selector] = ""  # Ensuring inclusion in the dictionary even if no content is found

    return structures


def main():
    # Load configuration
    config = load_config(CONFIG_PATH)

    # Fetch directory structures based on the provided URL and selectors
    docs_url = validate_and_get_docs_url(config)
    selectors = validate_and_get_selectors(config)
    structures = fetch_directory_structures(docs_url, selectors)

    # Display retrieved structures
    for selector, structure in structures.items():
        if structure:
            print(f"\nStructure for {selector}:\n{structure}\n")
        else:
            print(f"No structure found for {selector}.")


if __name__ == "__main__":
    main()
