#!/bin/bash

# Description:
# Automates staging, committing, and pushing changes to a branch. It checks for
# unstaged changes, stages any changes found, commits them with a standardized
# message, and attempts to push to the remote branch, setting a flag for PR creation.
#
# Assumptions:
# - The branch is already checked out and up-to-date with the target branch.
# - Required environment variables: AUTO_BRANCH and optionally DATE_FMT.

set -e  # Exit immediately if a command exits with a non-zero status.

# Ensure required variables are present
if [ -z "$AUTO_BRANCH" ]; then
  echo "Error: AUTO_BRANCH not set. Exiting..."
  exit 1
fi

echo "Staging changes..."
git add .

# Check for staged changes, exiting if none found
if git diff --staged --quiet; then
  echo "No changes to commit. Exiting..."
  echo "CREATE_PR=false" >> "$GITHUB_ENV"
  exit 0
fi

echo "Committing changes..."
COMMIT_MESSAGE="update: automated - Ansible project templates [${DATE_FMT:-$(date +%Y-%m-%d)}]"
git commit -m "$COMMIT_MESSAGE"
echo "Committed with message: '$COMMIT_MESSAGE'"

# Attempt to push changes to the specified branch
echo "Pushing to '$AUTO_BRANCH'..."
if git push --force origin "refs/heads/$AUTO_BRANCH" || \
   git push --set-upstream origin "$AUTO_BRANCH"; then
  echo "Push successful."
  CREATE_PR="true"
else
  echo "Push failed."
  CREATE_PR="false"
fi

# Set CREATE_PR flag for subsequent steps
echo "CREATE_PR=$CREATE_PR" >> "$GITHUB_ENV"