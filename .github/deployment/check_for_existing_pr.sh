#!/bin/bash

# Exit immediately if any command exits with a non-zero status.
set -e

# Check prerequisites
if [ -z "$GITHUB_TOKEN" ]; then
  echo "Error: GITHUB_TOKEN is not set."
  exit 1
fi

if [ -z "$AUTO_BRANCH" ]; then
  echo "Error: AUTO_BRANCH is not set."
  exit 1
fi

echo "Checking for existing PR from '$AUTO_BRANCH' to 'master'..."

# Fetch the list of PRs from AUTO_BRANCH to master, looking for the first one
PR_DATA=$(gh pr list --base master --head "$AUTO_BRANCH" --state all --json number,state --jq '.[0]')

# Check if there's any PR data
if [[ -z "$PR_DATA" ]]; then
  echo "No existing PR found. Proceeding with PR creation."
  echo "CREATE_PR=true" >> "$GITHUB_ENV"
else
  PR_NUMBER=$(echo "$PR_DATA" | jq -r .number)
  STATE=$(echo "$PR_DATA" | jq -r .state)

  # Check if the existing PR is open
  if [[ "$STATE" == "open" ]]; then
    echo "Existing PR is open. Skipping PR creation."
    echo "CREATE_PR=false" >> "$GITHUB_ENV"
  else
    # For closed PRs, check if they were merged
    MERGED_AT=$(gh pr view $PR_NUMBER --json mergedAt | jq -r '.mergedAt')
    if [[ "$MERGED_AT" != "null" ]]; then
      echo "Existing PR is closed and merged. Proceeding with PR creation."
      echo "CREATE_PR=true" >> "$GITHUB_ENV"
    else
      echo "Existing PR is closed and not merged. Skipping PR creation."
      echo "CREATE_PR=false" >> "$GITHUB_ENV"
    fi
  fi
fi
