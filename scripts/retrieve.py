from bs4 import BeautifulSoup

import requests
import configparser

# Load configuration
config = configparser.ConfigParser()
config.read('../config.ini')

# Configuration variables
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
        # Find all <pre> elements within the 'highlight' class containers below a given section id
        section = soup.find(id=selector)
        if section:
            code_blocks = section.find_all('div', class_='highlight')
            structure_text = '\n'.join(pre.get_text() for block in code_blocks for pre in block.find_all('pre'))
            structures[selector] = structure_text
        else:
            print(f"No section found for selector: {selector}")
            structures[selector] = ""

    return structures


if __name__ == "__main__":
    structures = fetch_directory_structures()
    for selector, structure in structures.items():
        if structure:
            print(f"\nStructure for {selector}:\n{structure}\n")
        else:
            print(f"No structure found for {selector}.")
