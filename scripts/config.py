import configparser
from pathlib import Path
from urllib.parse import urlparse


def load_config(config_path: str = 'config.ini') -> configparser.ConfigParser:
    """
    Loads the configuration file specified by `config_path`. This function initializes a
    ConfigParser object, checks for the existence of the configuration file, and then
    reads the configuration from the file.

    Args:
        config_path (str): The path to the configuration file. Defaults to 'config.ini'.

    Returns:
        configparser.ConfigParser: An instance of ConfigParser with the loaded configuration.

    Raises:
        FileNotFoundError: If the specified configuration file does not exist.
    """
    config_file_path = Path(config_path)
    if not config_file_path.is_file():
        raise FileNotFoundError(f"Configuration file not found at '{config_file_path.resolve()}'.")

    config = configparser.ConfigParser()
    config.read(config_file_path)
    return config


def validate_and_get_selectors(config):
    """
    Extracts selectors from the configuration object, ensuring they are properly formatted and valid.

    This function reads the 'SELECTORS' key from the 'DEFAULT' section of the provided configuration
    object. It splits this key's value into a list of selectors, trims any surrounding whitespace from
    each selector, and validates that at least one selector has been specified.

    Args:
        config (configparser.ConfigParser): The loaded configuration object.

    Returns:
        list: A list of trimmed selectors.

    Raises:
        KeyError: If the 'SELECTORS' key is missing from the configuration.
        ValueError: If no selectors are specified in the configuration.
    """
    # Attempt to retrieve and process the 'SELECTORS' configuration.
    try:
        selectors_raw = config['DEFAULT'].get('SELECTORS', '')
        selectors = [selector.strip() for selector in selectors_raw.split(',') if selector.strip()]

        if not selectors:
            raise ValueError("No selectors found in configuration. Ensure at least one selector is specified.")

    except KeyError as e:
        # Reraise with a more informative error message.
        raise KeyError(f"Missing required configuration key in 'DEFAULT' section: {e}")

    return selectors


def validate_and_get_docs_url(config):
    """
    Validates and retrieves the document URL from the configuration object.

    This function ensures that the 'DOCS_URL' key exists within the 'DEFAULT' section of the
    configuration object and that its value is a well-formed URL with an acceptable scheme (http or https).
    It aims to prevent errors by validating the URL's format and scheme before any attempt to use it
    in network operations.

    Args:
        config (configparser.ConfigParser): The loaded configuration object.

    Returns:
        str: The validated document URL.

    Raises:
        KeyError: If the 'DOCS_URL' key is missing from the configuration.
        ValueError: If the 'DOCS_URL' value is not a valid URL or uses an unsupported scheme.
    """
    try:
        docs_url = config['DEFAULT'].get('DOCS_URL', '').strip()
        if not docs_url:
            raise ValueError("The 'DOCS_URL' configuration is empty.")

        # Parse the URL and validate its scheme
        parsed_url = urlparse(docs_url)
        if not parsed_url.scheme or parsed_url.scheme not in ('http', 'https'):
            raise ValueError(f"The 'DOCS_URL' value '{docs_url}' is not a valid URL or uses an unsupported scheme.")

    except KeyError as e:
        raise KeyError(f"Missing required 'DOCS_URL' key in 'DEFAULT' section: {e}")

    return docs_url


def find_project_root(start_path: Path, marker: str = 'config.ini') -> str:
    """
    Finds the project root by looking for a marker file or directory, with error handling.

    This function traverses up the directory hierarchy from the given starting path until
    it finds the specified marker file or directory, indicating the project root. If the
    marker is not found by the time the root of the filesystem is reached, a FileNotFoundError
    is raised.

    Args:
        start_path (Path): The starting path from where to begin the search for the project root.
        marker (str): The name of the marker file or directory indicating the project root.

    Returns:
        str: The path to the project root as a string.

    Raises:
        FileNotFoundError: If the marker cannot be found in the path hierarchy.
    """
    current_path = start_path.resolve()

    while not (current_path / marker).exists():
        if current_path.parent == current_path:
            # We've reached the root of the filesystem without finding the marker
            raise FileNotFoundError(f"Unable to find the '{marker}' file or directory. "
                                    "Ensure you're running this within the project directory "
                                    "or check if the marker name is correct.")
        # Move up one level in the directory hierarchy
        current_path = current_path.parent

    return str(current_path)
