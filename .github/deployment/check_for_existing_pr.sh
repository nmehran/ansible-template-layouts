#!/bin/bash

# Description:
# Checks for the existence of an open or merged pull request (PR) from a specific branch to the master branch.
# Sets an environment variable indicating whether a new PR should be created based on the check results.
#
# Prerequisites:
# - GITHUB_TOKEN and AUTO_BRANCH environment variables must be set.
# - GitHub CLI (`gh`) installed and authenticated.

set -e  # Exit immediately if a command exits with a non-zero status.

# Validate prerequisites
if [ -z "$GITHUB_TOKEN" ] || [ -z "$AUTO_BRANCH" ]; then
  echo "Error: GITHUB_TOKEN and AUTO_BRANCH environment variables must be set."
  exit 1
fi

echo "Checking for existing PR from '$AUTO_BRANCH' to 'master'..."

# Fetch the first PR matching the criteria, if any
PR_DATA=$(gh pr list --base master --head "$AUTO_BRANCH" --state all --json number,state --limit 1)

# Check if there's any PR data
if [[ -z "$PR_DATA" ]]; then
  echo "No existing PR found. Proceeding with PR creation."
  CREATE_PR="true"
else
  # Parse the JSON output to extract PR number and state
  PR_NUMBER=$(echo "$PR_DATA" | jq -r '.[0].number')
  STATE=$(echo "$PR_DATA" | jq -r '.[0].state')

  if [[ "$STATE" == "open" ]]; then
    echo "An open PR already exists. Skipping PR creation."
    CREATE_PR="false"
  else
    # Fetch detailed information to check if the PR was merged
    MERGED_AT=$(gh pr view "$PR_NUMBER" --json mergedAt | jq -r '.mergedAt')
    if [[ "$MERGED_AT" != "null" ]]; then
      echo "Existing PR is closed and was merged. Eligible for a new PR creation."
      CREATE_PR="true"
    else
      echo "Existing PR is closed but not merged. No new PR will be created."
      CREATE_PR="false"
    fi
  fi
fi

# Export CREATE_PR decision for subsequent steps in the workflow
echo "CREATE_PR=$CREATE_PR" >> "$GITHUB_ENV"