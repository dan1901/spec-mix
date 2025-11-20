#!/bin/bash
# Setup script for git hooks

set -e

echo "🔧 Setting up Git hooks..."

# Configure git to use .githooks directory
git config core.hooksPath .githooks

echo "✅ Git hooks configured to use .githooks/ directory"
echo ""
echo "📝 Available hooks:"
echo "   - pre-commit: Runs markdown lint check before each commit"
echo ""
echo "🚀 To disable hooks temporarily, run:"
echo "   git config --unset core.hooksPath"
echo ""
echo "📦 To install markdown linter dependencies, run:"
echo "   npm install"
echo ""