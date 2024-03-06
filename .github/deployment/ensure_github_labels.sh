#!/bin/bash

# Description:
# This script ensures a specific set of GitHub labels exists in a repository. If a label does not exist,
# it is created with a predefined description and color. This script utilizes the GitHub CLI (`gh`) and is
# designed for GitHub Actions workflows.
#
# Prerequisites:
# - GitHub CLI (`gh`) must be installed and authenticated.
# - `GITHUB_TOKEN` with repo scope must be set in the environment.

# Ensure GitHub CLI is installed
if ! command -v gh &> /dev/null; then
  echo "Error: GitHub CLI ('gh') is not installed. Please install it to use this script."
  exit 1
fi

# Ensure GITHUB_TOKEN is set
if [ -z "${GITHUB_TOKEN}" ]; then
  echo "Error: GITHUB_TOKEN environment variable is not set."
  echo "Please ensure GITHUB_TOKEN is set with appropriate permissions."
  exit 1
fi

# Define the desired labels with their descriptions and colors
declare -A labels=(
  ["auto-update"]="Indicates an automatic update:ededed"
  ["template-change"]="Marks changes to template files:bfd4f2"
  ["needs-review"]="Requires review from maintainers:ffadad"
)

# Fetch all existing labels from the repository into an array
# Adjusting the `--limit` may be necessary for repositories with more than 100 labels.
existing_labels=$(gh label list --limit 100 | awk '{print $1}')

# Iterate over each label to ensure it exists
for label in "${!labels[@]}"; do
  IFS=':' read -r description color <<< "${labels[$label]}"
  echo "Ensuring label exists: $label"

  # Check if the label exists in the array of existing labels
  if echo "${existing_labels}" | grep -q "^${label}$"; then
    echo "Label '$label' already exists. Skipping creation."
  else
    echo "Creating label: $label"
    # Attempt to create the label with the specified description and color
    gh label create "$label" --description "$description" --color "$color"
  fi
done

echo "Label verification and creation process complete."
