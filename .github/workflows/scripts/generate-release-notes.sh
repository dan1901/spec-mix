#!/usr/bin/env bash
set -euo pipefail

# generate-release-notes.sh
# Generate release notes from git history
# Usage: generate-release-notes.sh <new_version> <last_tag>

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <new_version> <last_tag>" >&2
  exit 1
fi

NEW_VERSION="$1"
LAST_TAG="$2"

# Get commits since last tag
if [ "$LAST_TAG" = "v0.0.0" ] || [ "$LAST_TAG" = "$NEW_VERSION" ]; then
  # No previous tag or re-creating same version - show recent commits
  COMMIT_COUNT=$(git rev-list --count HEAD 2>/dev/null || echo "10")
  if [ "$COMMIT_COUNT" -gt 10 ]; then
    COMMITS=$(git log --oneline --pretty=format:"- %s" -n 10)
  else
    COMMITS=$(git log --oneline --pretty=format:"- %s" -n "$COMMIT_COUNT")
  fi
else
  COMMITS=$(git log --oneline --pretty=format:"- %s" $LAST_TAG..HEAD 2>/dev/null || git log --oneline --pretty=format:"- %s" -n 10)
fi

# Create release notes
cat > release_notes.md << EOF
This is the latest set of releases that you can use with your agent of choice. We recommend using the Specify CLI to scaffold your projects, however you can download these independently and manage them yourself.

## Changelog

$COMMITS

EOF

echo "Generated release notes:"
cat release_notes.md
