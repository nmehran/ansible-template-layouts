#!/bin/bash

# This script creates a pull request in a GitHub repository to update the Ansible project
# structure according to the latest guidelines. It is intended to be executed within a GitHub Actions
# environment, utilizing environment variables and the GitHub CLI.
#
# Prerequisites:
# - GitHub CLI (`gh`) must be installed and authenticated in the execution environment.
# - Required environment variables: DATE_FMT, AUTO_BRANCH, GITHUB_TOKEN, and GITHUB_ACTOR.

# Validate required environment variables are set
if [ -z "$DATE_FMT" ] || [ -z "$AUTO_BRANCH" ] || [ -z "$GITHUB_TOKEN" ] || [ -z "$GITHUB_ACTOR" ]; then
  echo "Error: One or more required environment variables are unset."
  echo "Ensure DATE_FMT, AUTO_BRANCH, GITHUB_TOKEN, and GITHUB_ACTOR are set."
  exit 1
fi

# Define the title of the pull request using the formatted date
PR_TITLE="Update Ansible Project Structure to Latest Guidelines [${DATE_FMT}]"

# Construct the body of the pull request
PR_BODY="This automated PR updates the \`ansible-template-layouts\` project directory structure to align with the latest official Ansible documentation as of ${DATE_FMT}.

### Changes Included:
- Updated templates to reflect the latest documentation standards.

For more details, please review the included changes."

# Execute the GitHub CLI command to create the pull request
if gh pr create \
   --title "$PR_TITLE" \
   --body "$PR_BODY" \
   --base master \
   --head "$AUTO_BRANCH" \
   --assignee "$GITHUB_ACTOR" \
   --reviewer "$GITHUB_ACTOR" \
   --label "auto-update,template-change,needs-review"; then
  echo "Pull request created successfully."
else
  echo "Failed to create pull request."
  exit 1
fi