#!/bin/bash

# This script automates the process of committing and pushing changes to a specified branch.
# It assumes the branch is already created and checked out, and it is up-to-date with the master branch.

# Exit immediately if any command exits with a non-zero status.
set -e

# Ensure AUTO_BRANCH is provided
if [ -z "$AUTO_BRANCH" ]; then
  echo "AUTO_BRANCH environment variable is not set. Exiting..."
  exit 1
fi

# Stage all changes for commit.
echo "Staging changes..."
git add .

# Check if there are any changes staged for commit. If not, exit the script.
if git diff --staged --quiet; then
  echo "No changes to commit. Exiting..."
  echo "CREATE_PR=false" >> "$GITHUB_ENV"
  exit 0
fi

# If the script reaches this point, there are changes to commit.
echo "Committing changes..."
git commit -m "update: automated - Ansible project templates [${DATE}]"
echo "Changes committed."

# Attempt to push changes to the remote branch, creating it if it doesn't exist.
echo "Pushing changes to '${AUTO_BRANCH}'..."
git push --force origin "refs/heads/${AUTO_BRANCH}:${AUTO_BRANCH}" || git push --set-upstream origin "refs/heads/${AUTO_BRANCH}"