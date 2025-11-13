---
description: Launch the Spec Kit web dashboard
scripts:
  sh: echo "Dashboard is managed via the specify CLI. Run: specify dashboard"
  ps: Write-Host "Dashboard is managed via the specify CLI. Run: specify dashboard"
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

This command helps you launch and manage the Spec Kit web dashboard, which provides a visual interface for monitoring features, kanban boards, and project artifacts.

## Dashboard Features

The dashboard provides:

1. **Features Overview**: View all features with their status and task counts
2. **Kanban Board**: Visualize task lanes (planned/doing/for_review/done) for each feature
3. **Artifact Viewer**: Read specifications, plans, and other documents
4. **Constitution**: View project principles and guidelines
5. **Auto-Refresh**: Real-time updates every 2 seconds

## Launching the Dashboard

### Quick Start
```bash
# Start dashboard and open in browser
specify dashboard
```

### Advanced Options
```bash
# Start on specific port
specify dashboard start --port 9000

# Start without opening browser
specify dashboard start

# Open browser manually
specify dashboard start --open
```

## Dashboard Commands

| Command | Description |
|---------|-------------|
| `specify dashboard` | Start dashboard and open browser (default) |
| `specify dashboard start` | Start dashboard server |
| `specify dashboard start --port <port>` | Start on specific port |
| `specify dashboard start --open` | Open in browser after start |
| `specify dashboard stop` | Stop running dashboard |
| `specify dashboard status` | Check if dashboard is running |

## Dashboard URL

Once started, the dashboard is available at:
```
http://localhost:9237
```

Or custom port if specified:
```
http://localhost:<PORT>
```

## What the Dashboard Shows

### Features View
- List of all features from `specs/` directory
- Features in worktrees (`.worktrees/`)
- Task counts by lane
- Available artifacts (spec, plan, tasks, etc.)

### Kanban Board
- Four lanes: Planned, Doing, For Review, Done
- Tasks (work packages) in each lane
- Task titles and IDs
- Click-through to view task details

### Artifacts
- Specification documents
- Implementation plans
- Task breakdowns
- Research notes
- Data models
- Acceptance reports

## Stopping the Dashboard

```bash
# Stop the dashboard
specify dashboard stop

# Or use Ctrl+C if running in foreground
```

## Dashboard Files

The dashboard stores state in:
```
.specify/
├── dashboard.pid    # Process ID
├── dashboard.port   # Current port
└── dashboard.token  # Shutdown authentication token
```

## Supported Workflows

### Monitoring Feature Progress
1. Start dashboard: `specify dashboard`
2. View features list
3. Click a feature to see kanban board
4. Watch tasks move through lanes in real-time

### Reviewing Artifacts
1. Open dashboard
2. Click artifact badge on feature card
3. Read rendered markdown content
4. Use back button to return

### Multi-Feature Development
1. Dashboard shows features from all worktrees
2. Each feature displays independently
3. Badge indicates which worktree (if any)

## Technical Details

- **Port Range**: Default 9237, auto-increments if busy
- **Refresh Rate**: 2 seconds for features list
- **Access**: localhost only (not exposed to network)
- **Shutdown**: Requires authentication token for security

## Integration with Workflow

The dashboard complements these commands:
- `/speckit.specify` - Creates features shown in dashboard
- `/speckit.implement` - Moves tasks through lanes
- `/speckit.review` - Changes task status visible in kanban
- `/speckit.accept` - Creates acceptance.md shown as artifact
- `/speckit.merge` - Completes feature lifecycle

## Troubleshooting

**Dashboard won't start:**
- Check if port is already in use: `specify dashboard status`
- Try different port: `specify dashboard start --port 9000`

**Features not showing:**
- Ensure `specs/` directory exists
- Check for `spec.md` in feature directories
- Refresh manually with button in UI

**Dashboard won't stop:**
- Use `specify dashboard stop`
- If stuck, find process: `lsof -i :9237`
- Kill manually: `kill <PID>`

## Example Session

```bash
# Start working on a feature
cd my-project
specify dashboard

# Dashboard opens showing your features

# In another terminal, work on features
/speckit.specify Build a new login page
/speckit.plan Use React and TypeScript
/speckit.implement

# Watch progress in dashboard as tasks move through lanes

# When done
# Dashboard auto-refreshes to show completed status
```

## Notes

- Dashboard is read-only (no editing via web UI)
- Markdown rendering uses marked.js library
- Auto-refresh can be disabled by closing dashboard
- Multi-language support (UI adapts to system locale)
