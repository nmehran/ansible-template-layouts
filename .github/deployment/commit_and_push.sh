#!/bin/bash

# This script automates the process of committing and pushing changes to a specified branch.
# It assumes the branch is already created and checked out, and it is up-to-date with the master branch.

# Exit immediately if any command exits with a non-zero status.
set -e

# Configure Git with the GitHub Actions bot's email and name for commit attribution.
git config --global user.email "action@github.com"
git config --global user.name "GitHub Action"

# Stage all changes for commit.
echo "Staging changes..."
git add .

# Commit the staged changes. If there are no changes, do not fail the script.
echo "Committing changes..."
git commit -m "update: automated - Ansible project templates [${DATE}]" || {
  echo "No changes to commit. Exiting..."
  exit 0  # Exit successfully as there's nothing to update.
}

# Push the commit to the remote repository.
echo "Pushing changes to '$NEW_BRANCH'..."
git push origin "$NEW_BRANCH" || echo "No changes to push."

echo "Update process completed successfully."
