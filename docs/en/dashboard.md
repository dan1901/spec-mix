# Web Dashboard

The Spec Mix dashboard provides a visual interface for managing and viewing your Spec-Driven Development workflow.

## Overview

The dashboard is a lightweight web server that displays your project's specifications, plans, and tasks in a beautiful, easy-to-navigate interface.

**Key Features:**

- 📊 Visual feature overview
- 📝 Markdown rendering
- 🔍 Quick navigation
- 🎨 Syntax highlighting
- 📱 Responsive design
- 🔄 Auto-refresh capability

## Quick Start

### Starting the Dashboard

```bash
# Default (port 8080)
spec-mix dashboard

# Custom port
spec-mix dashboard --port 3000

# Make accessible from network
spec-mix dashboard --host 0.0.0.0 --port 8080

# Auto-open browser
spec-mix dashboard --browser
```

### Accessing the Dashboard

Once started, open your browser to:

```text
http://localhost:8080
```

Or if using custom port:

```text
http://localhost:3000
```

### Stopping the Dashboard

Press `Ctrl+C` in the terminal, or use:

```bash
spec-mix dashboard --shutdown
```

## Dashboard Views

### Features List

The main view shows all features in your `specs/` directory:

```text
┌─────────────────────────────────────────────┐
│  Spec Mix Dashboard                         │
├─────────────────────────────────────────────┤
│                                             │
│  Features                                   │
│                                             │
│  ● 1-user-auth        [Specified]          │
│  ● 2-payment          [Planned]            │
│  ● 3-dashboard        [In Progress]        │
│  ○ 4-reports          [Not Started]        │
│                                             │
└─────────────────────────────────────────────┘
```

**Information Shown:**

- Feature number and name
- Current status
- Quick links to:
  - Specification (`spec.md`)
  - Plan (`plan.md`)
  - Tasks (`tasks.md`)
  - Other documents

**Status Indicators:**

- 🟢 Green - Completed
- 🟡 Yellow - In Progress
- 🔵 Blue - Planned
- ⚪ Gray - Not Started

### Document Viewer

Click any document to view it with full markdown rendering:

**Features:**

- Table of contents
- Syntax highlighting
- Code block formatting
- Link navigation
- Image display
- Table rendering

**Keyboard Shortcuts:**

- `←` - Back to features list
- `Esc` - Close document

## Command Options

### Basic Options

```bash
spec-mix dashboard [OPTIONS]
```

| Option | Description | Default |
|--------|-------------|---------|
| `--port` | Port number | 8080 |
| `--host` | Host address | localhost |
| `--browser` | Auto-open browser | false |
| `--shutdown` | Stop running dashboard | - |

### Examples

```bash
# Run on port 3000
spec-mix dashboard --port 3000

# Make accessible to team (network)
spec-mix dashboard --host 0.0.0.0

# Auto-open in browser
spec-mix dashboard --browser

# Custom port with auto-open
spec-mix dashboard --port 5000 --browser
```

## Use Cases

### During Development

Keep the dashboard running while working:

```bash
# Terminal 1: Dashboard
spec-mix dashboard

# Terminal 2: Development
cd specs/5-new-feature
# Work on specifications...

# View updates in browser at http://localhost:8080
```

### Team Demos

Share your screen showing the dashboard:

1. Start dashboard: `spec-mix dashboard --browser`
2. Navigate to feature overview
3. Click through specifications
4. Show progress and status

### Status Reviews

Use during standup or planning:

```bash
# Start dashboard
spec-mix dashboard --browser

# Review each feature's status
# Click through in-progress items
# Identify blockers
```

### Remote Access

Share dashboard with remote team:

```bash
# On your machine (check your IP first)
spec-mix dashboard --host 0.0.0.0 --port 8080

# Team members access via:
# http://YOUR_IP:8080
```

**Security Note:** Only use `--host 0.0.0.0` on trusted networks.

## Dashboard Structure

### Project Requirements

The dashboard expects this structure:

```text
your-project/
├── specs/
│   ├── 1-feature-one/
│   │   ├── spec.md
│   │   ├── plan.md
│   │   └── tasks.md
│   └── 2-feature-two/
│       ├── spec.md
│       └── plan.md
└── .spec-mix/
    └── memory/
        └── constitution.md
```

### Status Detection

Status is extracted from `spec.md`:

```markdown
**Status**: In Progress
```

Recognized statuses:

- `Not Started`
- `Specified`
- `Planned`
- `In Progress`
- `In Review`
- `Completed`
- `Blocked`
- `On Hold`

### Document Discovery

The dashboard automatically finds:

- All directories in `specs/`
- All `.md` files in each feature
- Constitution in `.spec-mix/memory/`

## Technical Details

### Architecture

- **Backend:** Python `http.server`
- **Frontend:** Vanilla JavaScript
- **Markdown:** marked.js library
- **Highlighting:** highlight.js
- **Styling:** Custom CSS

### File Locations

```text
src/specmix/
├── dashboard.py              # Server logic
├── dashboard_command.py      # CLI command
└── static/
    └── dashboard/
        ├── index.html        # Main page
        ├── app.js           # Frontend logic
        └── styles.css       # Styling
```

### API Endpoints

The dashboard provides a simple API:

```text
GET /                          # Main page
GET /api/features             # List all features
GET /api/feature/{name}       # Get feature details
GET /api/document/{feature}/{file}  # Get document content
GET /api/shutdown             # Stop server
```

### Data Flow

```text
Browser → JavaScript → API Endpoint → Python → File System
                    ←              ←        ←
```

## Customization

### Styling

Edit `src/specmix/static/dashboard/styles.css`:

```css
/* Change color scheme */
:root {
  --primary-color: #0066cc;
  --background: #ffffff;
  --text-color: #333333;
}
```

### Adding Features

Edit `src/specmix/static/dashboard/app.js`:

```javascript
// Add custom feature
async function loadCustomData() {
  // Your code here
}
```

### Custom Templates

Create custom document templates:

1. Add template to mission templates
2. Dashboard auto-discovers it
3. Appears in feature document list

## Troubleshooting

### Dashboard won't start

```bash
# Check if port is in use
lsof -i :8080

# Use different port
spec-mix dashboard --port 8081
```

### Features not showing

```bash
# Verify specs directory exists
ls specs/

# Check directory naming (should be number-name format)
ls specs/ | grep -E '^[0-9]+-'
```

### Documents not rendering

1. Check markdown file exists
2. Verify file encoding is UTF-8
3. Check for syntax errors in markdown

### Can't access from other machines

```bash
# Make sure using correct host
spec-mix dashboard --host 0.0.0.0

# Check firewall settings
# Verify network connectivity
ping YOUR_IP
```

### Port already in use

```bash
# Find what's using the port
lsof -i :8080

# Kill the process or use different port
spec-mix dashboard --port 8081
```

## Advanced Usage

### Integration with CI/CD

Generate static HTML for CI/CD:

```bash
# Future feature
spec-mix dashboard --export ./dashboard-static/
```

### Automated Testing

```bash
# Test dashboard starts correctly
spec-mix dashboard --test

# Verify API endpoints
curl http://localhost:8080/api/features
```

### Performance

The dashboard is optimized for:

- **Projects:** Up to 100 features
- **Documents:** Up to 1MB each
- **Concurrent users:** Up to 10

For larger projects, consider:

- Breaking into multiple projects
- Using static site generation
- Implementing caching

## Security Considerations

### Local Development

Safe defaults for local use:

```bash
# Only accessible from your machine
spec-mix dashboard  # Uses localhost
```

### Team Sharing

When sharing with team:

```bash
# Only on trusted networks
spec-mix dashboard --host 0.0.0.0
```

**Don't:**

- Expose to public internet
- Use on untrusted networks
- Share sensitive specifications publicly

**Do:**

- Use VPN for remote access
- Implement authentication (future feature)
- Review specifications before sharing

## Future Features

Planned enhancements:

- 🔐 Authentication/authorization
- 📊 Progress charts and metrics
- 🔍 Full-text search
- 📤 Export to PDF/HTML
- 🎨 Themes and customization
- 🔄 Real-time file watching
- 💬 Comments and annotations
- 📱 Mobile app

## Best Practices

### During Development

1. Keep dashboard running in background
2. Refresh after saving documents
3. Use for quick reference
4. Share URL for pair programming

### For Reviews

1. Use for sprint reviews
2. Walk through features visually
3. Show progress to stakeholders
4. Get feedback on specifications

### For Documentation

1. Use as living documentation
2. Share with new team members
3. Reference during planning
4. Archive completed features

## Next Steps

- [Enhanced Features Overview](features.md)
- [Mission System](missions.md)
- [Quick Start](quickstart.md)
- [Local Development](local-development.md)
