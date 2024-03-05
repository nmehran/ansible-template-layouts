#!/bin/bash

# This script checks for an existing pull request (PR) from a specified branch to the master branch.
# It uses the GitHub CLI to query for existing PRs and sets an environment variable to indicate
# whether a new PR should be created.

# Exit immediately if any command exits with a non-zero status.
set -e

# Check prerequisites
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GITHUB_TOKEN is not set."
    exit 1
fi

if [ -z "$NEW_BRANCH" ]; then
    echo "Error: NEW_BRANCH is not set."
    exit 1
fi

# Configure the GitHub CLI to use the provided token
export GITHUB_TOKEN

echo "Checking for existing PR from '$NEW_BRANCH' to 'master'..."

# Fetch the list of PRs from NEW_BRANCH to master, looking for the first one
PR_DATA=$(gh pr list --head "$NEW_BRANCH" --base master --state all --json url,state,mergedAt --jq '.[0]')

# Determine action based on the existence and state of the PR
if [[ "$PR_DATA" == "" ]]; then
    echo "No existing PR found. Proceeding with PR creation."
else
    STATE=$(echo "$PR_DATA" | jq -r '.state')
    MERGED_AT=$(echo "$PR_DATA" | jq -r '.mergedAt')
    if [[ "$STATE" == "closed" && "$MERGED_AT" == "null" ]]; then
        echo "Existing PR is closed and not merged. Skipping PR creation."
    elif [[ "$STATE" == "open" ]]; then
        echo "Existing PR is open. Skipping PR creation."
    else
        echo "Existing PR is either merged or not applicable. Proceeding with PR creation."
    fi
fi
