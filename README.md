# Ansible Template Skeletons

## Overview
`ansible-template-skeletons` is an automated tool designed to keep your Ansible project's directory structure in sync with the latest recommendations from the official Ansible documentation. Utilizing GitHub Actions, this project checks the Ansible documentation daily for changes in the recommended project layout and automatically updates this repository to reflect those changes, ensuring best practices are always followed.

## Features
- **Automated Updates**: Leveraging GitHub Actions to regularly check the Ansible documentation for any updates or changes in the directory structure.
- **Pull Request Management**: Automatically generates pull requests for changes, allowing for human review before merging.
- **Version Tagging**: Upon acceptance and merging of changes, the project is tagged with the current date, marking the version of the directory structure.
