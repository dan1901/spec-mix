#!/usr/bin/env bash
set -euo pipefail

# create-github-release.sh
# Create a GitHub release with all template zip files
# Usage: create-github-release.sh <version>

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version>" >&2
  exit 1
fi

VERSION="$1"

# Remove 'v' prefix from version for release title
VERSION_NO_V=${VERSION#v}

gh release create "$VERSION" \
  .genreleases/spec-mix-template-copilot-sh-"$VERSION".zip \
  .genreleases/spec-mix-template-copilot-ps-"$VERSION".zip \
  .genreleases/spec-mix-template-claude-sh-"$VERSION".zip \
  .genreleases/spec-mix-template-claude-ps-"$VERSION".zip \
  .genreleases/spec-mix-template-gemini-sh-"$VERSION".zip \
  .genreleases/spec-mix-template-gemini-ps-"$VERSION".zip \
  .genreleases/spec-mix-template-cursor-agent-sh-"$VERSION".zip \
  .genreleases/spec-mix-template-cursor-agent-ps-"$VERSION".zip \
  .genreleases/spec-mix-template-opencode-sh-"$VERSION".zip \
  .genreleases/spec-mix-template-opencode-ps-"$VERSION".zip \
  .genreleases/spec-mix-template-qwen-sh-"$VERSION".zip \
  .genreleases/spec-mix-template-qwen-ps-"$VERSION".zip \
  .genreleases/spec-mix-template-windsurf-sh-"$VERSION".zip \
  .genreleases/spec-mix-template-windsurf-ps-"$VERSION".zip \
  .genreleases/spec-mix-template-codex-sh-"$VERSION".zip \
  .genreleases/spec-mix-template-codex-ps-"$VERSION".zip \
  .genreleases/spec-mix-template-kilocode-sh-"$VERSION".zip \
  .genreleases/spec-mix-template-kilocode-ps-"$VERSION".zip \
  .genreleases/spec-mix-template-auggie-sh-"$VERSION".zip \
  .genreleases/spec-mix-template-auggie-ps-"$VERSION".zip \
  .genreleases/spec-mix-template-roo-sh-"$VERSION".zip \
  .genreleases/spec-mix-template-roo-ps-"$VERSION".zip \
  .genreleases/spec-mix-template-codebuddy-sh-"$VERSION".zip \
  .genreleases/spec-mix-template-codebuddy-ps-"$VERSION".zip \
  .genreleases/spec-mix-template-amp-sh-"$VERSION".zip \
  .genreleases/spec-mix-template-amp-ps-"$VERSION".zip \
  .genreleases/spec-mix-template-q-sh-"$VERSION".zip \
  .genreleases/spec-mix-template-q-ps-"$VERSION".zip \
  --title "Spec Mix Templates - $VERSION_NO_V" \
  --notes-file release_notes.md
