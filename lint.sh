#!/bin/bash
# Local markdown lint check script

set -e

echo "🔍 Checking markdown files..."
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to run lint
run_lint() {
    local fix_mode=${1:-""}

    if [ "$fix_mode" = "--fix" ]; then
        echo "🔧 Running markdown lint with auto-fix..."
        if command_exists markdownlint-cli2; then
            markdownlint-cli2 --fix '**/*.md'
        elif command_exists npx; then
            npx markdownlint-cli2 --fix '**/*.md'
        fi
    else
        echo "📋 Running markdown lint check..."
        if command_exists markdownlint-cli2; then
            markdownlint-cli2 '**/*.md'
        elif command_exists npx; then
            npx markdownlint-cli2 '**/*.md'
        fi
    fi
}

# Check if markdownlint-cli2 is available
if ! command_exists markdownlint-cli2 && ! command_exists npx; then
    echo "❌ markdownlint-cli2 is not installed"
    echo ""
    echo "📦 Please install dependencies first:"
    echo "   npm install"
    echo ""
    echo "Or install globally:"
    echo "   npm install -g markdownlint-cli2"
    exit 1
fi

# Run lint with optional fix mode
run_lint "$1"
LINT_EXIT=$?

if [ $LINT_EXIT -eq 0 ]; then
    echo ""
    echo "✅ All markdown files passed lint check!"
else
    echo ""
    echo "❌ Some markdown files have lint issues"
    echo ""
    echo "💡 To automatically fix issues, run:"
    echo "   ./lint.sh --fix"
    exit $LINT_EXIT
fi