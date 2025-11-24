#!/usr/bin/env bash
set -euo pipefail

# check-release-exists.sh
# Check if a GitHub release already exists for the given version
# If it exists, delete it to allow re-creation
# Usage: check-release-exists.sh <version>

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version>" >&2
  exit 1
fi

VERSION="$1"

if gh release view "$VERSION" >/dev/null 2>&1; then
  echo "Release $VERSION already exists, deleting for re-creation..."
  gh release delete "$VERSION" --yes --cleanup-tag 2>/dev/null || true
  echo "exists=false" >> $GITHUB_OUTPUT
  echo "Deleted existing release, proceeding with re-creation..."
else
  echo "exists=false" >> $GITHUB_OUTPUT
  echo "Release $VERSION does not exist, proceeding..."
fi
