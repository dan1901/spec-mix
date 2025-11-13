#!/usr/bin/env bash
# Move task between lanes (planned → doing → for_review → done)
# Usage: move-task.sh <TASK_ID> <FROM_LANE> <TO_LANE> <FEATURE_DIR>

set -e

TASK_ID="$1"
FROM_LANE="$2"
TO_LANE="$3"
FEATURE_DIR="$4"

if [[ -z "$TASK_ID" || -z "$FROM_LANE" || -z "$TO_LANE" || -z "$FEATURE_DIR" ]]; then
    echo "Usage: $0 <TASK_ID> <FROM_LANE> <TO_LANE> <FEATURE_DIR>"
    echo ""
    echo "Lanes: planned, doing, for_review, done"
    echo ""
    echo "Example: $0 WP01 planned doing specs/001-feature"
    exit 1
fi

# Validate lanes
VALID_LANES=("planned" "doing" "for_review" "done")
if [[ ! " ${VALID_LANES[@]} " =~ " ${FROM_LANE} " ]]; then
    echo "Error: Invalid FROM_LANE: $FROM_LANE" >&2
    echo "Valid lanes: ${VALID_LANES[*]}" >&2
    exit 1
fi

if [[ ! " ${VALID_LANES[@]} " =~ " ${TO_LANE} " ]]; then
    echo "Error: Invalid TO_LANE: $TO_LANE" >&2
    echo "Valid lanes: ${VALID_LANES[*]}" >&2
    exit 1
fi

FROM_DIR="$FEATURE_DIR/tasks/$FROM_LANE"
TO_DIR="$FEATURE_DIR/tasks/$TO_LANE"
TASK_FILE="$TASK_ID.md"

# Create task directories if they don't exist
mkdir -p "$FROM_DIR" "$TO_DIR"

# Check if task exists
if [[ ! -f "$FROM_DIR/$TASK_FILE" ]]; then
    echo "Error: Task $TASK_FILE not found in $FROM_DIR" >&2
    exit 1
fi

# Move task
mv "$FROM_DIR/$TASK_FILE" "$TO_DIR/$TASK_FILE"

# Update frontmatter
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Update lane
if command -v sed &> /dev/null; then
    # macOS and Linux compatible sed
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/^lane: .*$/lane: $TO_LANE/" "$TO_DIR/$TASK_FILE"
    else
        sed -i "s/^lane: .*$/lane: $TO_LANE/" "$TO_DIR/$TASK_FILE"
    fi
fi

# Update timestamps based on lane
case "$TO_LANE" in
    doing)
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s/^started_at:.*$/started_at: $TIMESTAMP/" "$TO_DIR/$TASK_FILE"
        else
            sed -i "s/^started_at:.*$/started_at: $TIMESTAMP/" "$TO_DIR/$TASK_FILE"
        fi
        ;;
    done)
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s/^completed_at:.*$/completed_at: $TIMESTAMP/" "$TO_DIR/$TASK_FILE"
        else
            sed -i "s/^completed_at:.*$/completed_at: $TIMESTAMP/" "$TO_DIR/$TASK_FILE"
        fi
        ;;
esac

# Append activity log
echo "" >> "$TO_DIR/$TASK_FILE"
echo "- $TIMESTAMP: Moved from $FROM_LANE to $TO_LANE" >> "$TO_DIR/$TASK_FILE"

echo "✅ Task $TASK_ID moved: $FROM_LANE → $TO_LANE"
echo "📝 File: $TO_DIR/$TASK_FILE"
