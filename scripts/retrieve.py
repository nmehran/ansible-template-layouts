import requests
from bs4 import BeautifulSoup
import configparser

# Create a ConfigParser object and read the config.ini file
config = configparser.ConfigParser()
config.read('../config.ini')

# Accessing variables
docs_url = config['DEFAULT']['DOCS_URL']
selectors = [selector.strip() for selector in config['DEFAULT']['SELECTORS'].split(',')]


def fetch_directory_structures():
    response = requests.get(docs_url)
    if response.status_code != 200:
        print(f"Failed to fetch the webpage, status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    structures = {}

    for selector in selectors:
        directory_structure_element = soup.find(id=selector)
        if directory_structure_element:
            structures[selector] = directory_structure_element.get_text()
        else:
            print(f"No element found for selector: {selector}")

    return structures


if __name__ == "__main__":
    structures = fetch_directory_structures()
    for selector, structure in structures.items():
        if structure:
            print(f"Structure for {selector}:\n{structure}\n")
        else:
            print(f"No structure found for {selector}.")
