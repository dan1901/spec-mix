#!/usr/bin/env bash
set -euo pipefail

# get-next-version.sh
# Get version from pyproject.toml and compare with latest git tag
# Only create release if versions differ
# Usage: get-next-version.sh

# Get the latest tag, or use v0.0.0 if no tags exist
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
LATEST_VERSION=$(echo $LATEST_TAG | sed 's/v//')
echo "latest_tag=$LATEST_TAG" >> $GITHUB_OUTPUT
echo "Latest git tag: $LATEST_TAG"

# Read version from pyproject.toml
if [ ! -f "pyproject.toml" ]; then
    echo "Error: pyproject.toml not found"
    exit 1
fi

# Extract version from pyproject.toml (handles both quoted and unquoted values)
PYPROJECT_VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = //; s/"//g; s/'"'"'//g' | tr -d ' ')

if [ -z "$PYPROJECT_VERSION" ]; then
    echo "Error: Could not read version from pyproject.toml"
    exit 1
fi

echo "Version in pyproject.toml: $PYPROJECT_VERSION"

# Add 'v' prefix if not present
if [[ $PYPROJECT_VERSION != v* ]]; then
    NEW_VERSION="v$PYPROJECT_VERSION"
else
    NEW_VERSION="$PYPROJECT_VERSION"
fi

# Compare versions
if [ "$LATEST_VERSION" == "$PYPROJECT_VERSION" ] || [ "$LATEST_TAG" == "$NEW_VERSION" ]; then
    echo "✓ Version unchanged ($PYPROJECT_VERSION) - will re-create release if exists"
else
    echo "✓ Version changed: $LATEST_VERSION → $PYPROJECT_VERSION"
fi

# Always allow release (check-release-exists.sh handles deletion if needed)
echo "should_release=true" >> $GITHUB_OUTPUT
echo "new_version=$NEW_VERSION" >> $GITHUB_OUTPUT
