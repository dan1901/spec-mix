"""
Dashboard server for Spec Kit.

Provides a web-based interface to view features, kanban boards, and artifacts.
"""

import os
import json
import secrets
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Dict, List, Any, Optional
import threading
import signal
import sys

# Dashboard configuration
DEFAULT_PORT = 9237
MAX_PORT_ATTEMPTS = 100


class DashboardHandler(BaseHTTPRequestHandler):
    """HTTP request handler for dashboard"""

    def log_message(self, format, *args):
        """Override to customize logging"""
        # Only log errors
        if args[1][0] not in ('2', '3'):
            super().log_message(format, *args)

    def do_GET(self):
        """Handle GET requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        # Route requests
        if path == '/':
            self.serve_dashboard_html()
        elif path == '/api/health':
            self.serve_health()
        elif path == '/api/features':
            self.serve_features()
        elif path.startswith('/api/kanban/'):
            feature_id = path.split('/')[-1]
            self.serve_kanban(feature_id)
        elif path.startswith('/api/artifact/'):
            parts = path.split('/')[3:]  # Skip '', 'api', 'artifact'
            if len(parts) >= 2:
                feature_id = parts[0]
                artifact_name = '/'.join(parts[1:])
                self.serve_artifact(feature_id, artifact_name)
        elif path.startswith('/api/task/'):
            parts = path.split('/')[3:]  # Skip '', 'api', 'task'
            if len(parts) >= 3:
                feature_id = parts[0]
                lane = parts[1]
                task_id = parts[2]

                # Check for sub-paths: commits, files, diff, reviews
                if len(parts) >= 4:
                    subpath = parts[3]
                    if subpath == 'commits':
                        self.serve_task_commits(feature_id, lane, task_id)
                    elif subpath == 'files':
                        self.serve_task_files(feature_id, lane, task_id)
                    elif subpath == 'reviews':
                        self.serve_task_reviews(feature_id, lane, task_id)
                    elif subpath == 'diff' and len(parts) >= 5:
                        commit_sha = parts[4]
                        self.serve_commit_diff(commit_sha)
                    else:
                        self.send_error(404, "Not found")
                else:
                    self.serve_task_detail(feature_id, lane, task_id)
        elif path.startswith('/api/diff/'):
            commit_sha = path.split('/')[-1]
            self.serve_commit_diff(commit_sha)
        elif path == '/api/untracked-commits':
            self.serve_untracked_commits()
        elif path == '/api/constitution':
            self.serve_constitution()
        elif path == '/api/i18n/current':
            self.serve_i18n()
        elif path.startswith('/static/'):
            self.serve_static(path[8:])  # Remove '/static/'
        else:
            self.send_error(404, "Not found")

    def do_POST(self):
        """Handle POST requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        if path == '/api/shutdown':
            self.handle_shutdown()
        else:
            self.send_error(404, "Not found")

    def serve_dashboard_html(self):
        """Serve the main dashboard HTML"""
        static_dir = Path(__file__).parent / 'static' / 'dashboard'
        html_file = static_dir / 'index.html'

        if html_file.exists():
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open(html_file, 'rb') as f:
                self.wfile.write(f.read())
        else:
            # Fallback minimal HTML if file doesn't exist yet
            html = """<!DOCTYPE html>
<html>
<head>
    <title>Spec Mix Dashboard</title>
    <meta charset="utf-8">
    <style>
        body { font-family: system-ui, -apple-system, sans-serif; margin: 40px; }
        h1 { color: #333; }
    </style>
</head>
<body>
    <h1>Spec Mix Dashboard</h1>
    <p>Dashboard is running. Frontend files will be added next.</p>
</body>
</html>"""
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))

    def serve_health(self):
        """Health check endpoint"""
        data = {
            'status': 'ok',
            'project_path': str(Path.cwd()),
            'token': getattr(self.server, 'shutdown_token', None)
        }
        self.send_json(data)

    def serve_features(self):
        """List all features"""
        features = scan_all_features()
        self.send_json(features)

    def serve_kanban(self, feature_id: str):
        """Get kanban board for a feature"""
        kanban_data = scan_feature_kanban(feature_id)
        self.send_json(kanban_data)

    def serve_artifact(self, feature_id: str, artifact_name: str):
        """Serve a specific artifact"""
        content = get_artifact_content(feature_id, artifact_name)
        if content is not None:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        else:
            self.send_error(404, f"Artifact not found: {artifact_name}")

    def serve_task_detail(self, feature_id: str, lane: str, task_id: str):
        """Serve detailed information about a specific task"""
        task_detail = get_task_detail(feature_id, lane, task_id)
        if task_detail is not None:
            self.send_json(task_detail)
        else:
            self.send_error(404, f"Task not found: {task_id}")

    def serve_task_commits(self, feature_id: str, lane: str, task_id: str):
        """Serve git commits for a task"""
        commits = get_task_commits(feature_id, task_id)
        self.send_json(commits)

    def serve_task_files(self, feature_id: str, lane: str, task_id: str):
        """Serve modified files for a task"""
        files = get_task_files(feature_id, task_id)
        self.send_json(files)

    def serve_commit_diff(self, commit_sha: str):
        """Serve diff for a specific commit"""
        diff = get_commit_diff(commit_sha)
        if diff is not None:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(diff.encode('utf-8'))
        else:
            self.send_error(404, f"Commit not found: {commit_sha}")

    def serve_task_reviews(self, feature_id: str, lane: str, task_id: str):
        """Serve review history for a task"""
        reviews = get_task_reviews(feature_id, task_id)
        self.send_json(reviews)

    def serve_constitution(self):
        """Serve project constitution with fallback paths"""
        # Try multiple locations in priority order
        paths = [
            Path('specs/constitution.md'),      # User project (priority 1)
            Path('constitution.md'),            # Root level (priority 2)
            Path('memory/constitution.md')      # Template/example (priority 3)
        ]

        for constitution_path in paths:
            if constitution_path.exists():
                try:
                    with open(constitution_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    # Add header indicating source
                    source_note = f"<!-- Loaded from: {constitution_path} -->\n\n"
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain; charset=utf-8')
                    self.end_headers()
                    self.wfile.write((source_note + content).encode('utf-8'))
                    return
                except Exception as e:
                    # Continue to next path if read fails
                    continue

        # No constitution found - send helpful message
        helpful_msg = """# No Constitution Found

Create a project constitution by running:
- `/spec-mix.constitution` command in your project
- Or manually create `specs/constitution.md`

This file defines your project's core principles and governance.

## Why Constitution?

A project constitution establishes:
- Core principles and values
- Development standards
- Quality requirements
- Governance rules

## Getting Started

Run `/spec-mix.constitution` to create one interactively, or use the template at:
`.spec-mix/active-mission/constitution/constitution-template.md`
"""

        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(helpful_msg.encode('utf-8'))

    def serve_i18n(self):
        """Serve i18n strings for dashboard UI"""
        try:
            from .i18n import get_locale_manager
            locale_mgr = get_locale_manager()

            # Get dashboard-specific strings
            strings = {
                'title': locale_mgr.get('cli.dashboard.title', 'Spec Mix Dashboard'),
                'features': locale_mgr.get('cli.dashboard.features', 'Features'),
                'kanban': locale_mgr.get('cli.dashboard.kanban', 'Kanban Board'),
                'artifacts': locale_mgr.get('cli.dashboard.artifacts', 'Artifacts'),
                'constitution': locale_mgr.get('cli.dashboard.constitution', 'Constitution'),
                'no_features': locale_mgr.get('cli.dashboard.no_features', 'No features found'),
                'lanes': {
                    'planned': locale_mgr.get('cli.dashboard.lanes.planned', 'Planned'),
                    'doing': locale_mgr.get('cli.dashboard.lanes.doing', 'Doing'),
                    'for_review': locale_mgr.get('cli.dashboard.lanes.for_review', 'For Review'),
                    'done': locale_mgr.get('cli.dashboard.lanes.done', 'Done')
                }
            }
            self.send_json(strings)
        except:
            # Fallback to English if i18n not available
            self.send_json({
                'title': 'Spec Mix Dashboard',
                'features': 'Features',
                'kanban': 'Kanban Board',
                'artifacts': 'Artifacts',
                'constitution': 'Constitution',
                'no_features': 'No features found',
                'lanes': {
                    'planned': 'Planned',
                    'doing': 'Doing',
                    'for_review': 'For Review',
                    'done': 'Done'
                }
            })

    def serve_untracked_commits(self):
        """Serve list of commits without Work Package IDs"""
        commits = get_untracked_commits()
        self.send_json(commits)

    def serve_static(self, path: str):
        """Serve static files"""
        static_dir = Path(__file__).parent / 'static' / 'dashboard'
        file_path = static_dir / path

        # Security: prevent directory traversal
        try:
            file_path = file_path.resolve()
            static_dir = static_dir.resolve()
            if not str(file_path).startswith(str(static_dir)):
                self.send_error(403, "Forbidden")
                return
        except:
            self.send_error(400, "Invalid path")
            return

        if file_path.exists() and file_path.is_file():
            # Determine content type
            suffix = file_path.suffix.lower()
            content_types = {
                '.html': 'text/html',
                '.css': 'text/css',
                '.js': 'application/javascript',
                '.json': 'application/json',
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.svg': 'image/svg+xml',
            }
            content_type = content_types.get(suffix, 'application/octet-stream')

            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            with open(file_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, "File not found")

    def handle_shutdown(self):
        """Handle shutdown request"""
        # Read token from request body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')

        try:
            data = json.loads(body) if body else {}
            provided_token = data.get('token')
        except:
            provided_token = None

        server_token = getattr(self.server, 'shutdown_token', None)

        if provided_token == server_token:
            self.send_json({'status': 'shutting down'})
            # Shutdown in a separate thread to allow response to be sent
            threading.Thread(target=self.server.shutdown, daemon=True).start()
        else:
            self.send_error(403, "Invalid shutdown token")

    def send_json(self, data: Any):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))


def get_hotfix_info(hotfix_dir: Path) -> Optional[Dict[str, Any]]:
    """Get information about the hotfix directory"""
    try:
        hotfix_files = list(hotfix_dir.glob('HOTFIX-*.md'))
        if not hotfix_files:
            return None

        # Count hotfixes by status (parse frontmatter)
        status_counts = {'analyzing': 0, 'planning': 0, 'implementing': 0, 'verifying': 0, 'done': 0}
        hotfixes = []

        for hf_file in hotfix_files:
            try:
                with open(hf_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Parse frontmatter
                status = 'analyzing'
                priority = 'P2'
                if content.startswith('---'):
                    lines = content.split('\n')
                    for line in lines[1:]:
                        if line.strip() == '---':
                            break
                        if line.startswith('status:'):
                            status = line.split(':')[1].strip()
                        elif line.startswith('priority:'):
                            priority = line.split(':')[1].strip()

                status_counts[status] = status_counts.get(status, 0) + 1
                hotfixes.append({
                    'id': hf_file.stem,
                    'status': status,
                    'priority': priority,
                    'path': str(hf_file)
                })
            except:
                pass

        return {
            'id': 'hotfix',
            'name': 'Hotfixes',
            'path': str(hotfix_dir),
            'worktree': None,
            'mode': 'hotfix',
            'is_hotfix_dir': True,
            'artifacts': {'fixes': True},
            'fixes_count': len(hotfix_files),
            'hotfixes': hotfixes,
            'status_counts': status_counts,
            'kanban_stats': {
                'planned': status_counts.get('analyzing', 0) + status_counts.get('planning', 0),
                'doing': status_counts.get('implementing', 0),
                'for_review': status_counts.get('verifying', 0),
                'done': status_counts.get('done', 0)
            },
            'total_tasks': len(hotfix_files)
        }
    except Exception as e:
        print(f"Error reading hotfix directory {hotfix_dir}: {e}")
        return None


def scan_all_features() -> List[Dict[str, Any]]:
    """Scan for all features in specs/ and .worktrees/"""
    features = []

    # Scan specs/ directory
    specs_dir = Path('specs')
    if specs_dir.exists():
        for feature_dir in specs_dir.iterdir():
            if feature_dir.is_dir() and not feature_dir.name.startswith('.'):
                # Skip hotfix directory - handle separately
                if feature_dir.name == 'hotfix':
                    # Scan hotfix directory for HOTFIX-*.md files
                    hotfix_info = get_hotfix_info(feature_dir)
                    if hotfix_info:
                        features.append(hotfix_info)
                    continue
                feature_info = get_feature_info(feature_dir)
                if feature_info:
                    features.append(feature_info)

    # Scan .worktrees/*/specs/ directories
    worktrees_dir = Path('.worktrees')
    if worktrees_dir.exists():
        for worktree_dir in worktrees_dir.iterdir():
            if worktree_dir.is_dir():
                worktree_specs = worktree_dir / 'specs'
                if worktree_specs.exists():
                    for feature_dir in worktree_specs.iterdir():
                        if feature_dir.is_dir() and not feature_dir.name.startswith('.'):
                            feature_info = get_feature_info(feature_dir, worktree=worktree_dir.name)
                            if feature_info:
                                features.append(feature_info)

    return features


def get_feature_info(feature_path: Path, worktree: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Get information about a feature"""
    try:
        # Read project mode from config
        project_mode = 'pro'  # Default
        config_file = Path('.spec-mix') / 'config.json'
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    project_mode = config.get('mode', 'pro')
            except:
                pass

        info = {
            'id': feature_path.name,
            'name': feature_path.name,
            'path': str(feature_path),
            'worktree': worktree,
            'mode': project_mode,
            'artifacts': {}
        }

        # Check for common artifacts
        artifacts = ['spec.md', 'plan.md', 'tasks.md', 'research.md',
                    'data-model.md', 'acceptance.md', 'checklist.md', 'walkthrough.md']

        for artifact in artifacts:
            info['artifacts'][artifact.replace('.md', '')] = (feature_path / artifact).exists()

        # Check for fixes directory
        fixes_dir = feature_path / 'fixes'
        fixes_count = 0
        if fixes_dir.exists() and fixes_dir.is_dir():
            fixes_count = len(list(fixes_dir.glob('FIX*.md')))
        info['fixes_count'] = fixes_count
        info['artifacts']['fixes'] = fixes_dir.exists() and fixes_count > 0

        # Check for phase-based walkthroughs (Normal mode)
        phase_walkthroughs = list(feature_path.glob('walkthrough-phase-*.md'))
        info['artifacts']['phase_walkthroughs'] = len(phase_walkthroughs)
        info['walkthrough_files'] = [f.name for f in phase_walkthroughs]

        # Check for kanban (either directory or tasks.md file)
        tasks_dir = feature_path / 'tasks'
        tasks_file = feature_path / 'tasks.md'
        info['artifacts']['kanban'] = tasks_dir.exists() or tasks_file.exists()

        # Count tasks by lane
        kanban_stats = {'planned': 0, 'doing': 0, 'for_review': 0, 'done': 0}

        if tasks_dir.exists() and tasks_dir.is_dir():
            # Directory-based kanban
            has_lane_dirs = any((tasks_dir / lane).exists() for lane in ['planned', 'doing', 'for_review', 'done'])
            if has_lane_dirs:
                kanban_stats = {
                    'planned': len(list((tasks_dir / 'planned').glob('*.md'))) if (tasks_dir / 'planned').exists() else 0,
                    'doing': len(list((tasks_dir / 'doing').glob('*.md'))) if (tasks_dir / 'doing').exists() else 0,
                    'for_review': len(list((tasks_dir / 'for_review').glob('*.md'))) if (tasks_dir / 'for_review').exists() else 0,
                    'done': len(list((tasks_dir / 'done').glob('*.md'))) if (tasks_dir / 'done').exists() else 0
                }
        elif tasks_file.exists():
            # Single tasks.md file - parse it to count tasks
            kanban_data = parse_tasks_markdown(tasks_file)
            kanban_stats = {
                'planned': len(kanban_data['lanes']['planned']),
                'doing': len(kanban_data['lanes']['doing']),
                'for_review': len(kanban_data['lanes']['for_review']),
                'done': len(kanban_data['lanes']['done'])
            }

            # Check if it's phase-based mode
            if kanban_data.get('is_phase_mode'):
                info['is_phase_mode'] = True
                info['phases'] = kanban_data.get('phases', {})
                info['task_mode'] = 'phase'
            else:
                info['is_phase_mode'] = False
                info['task_mode'] = 'kanban'

        info['kanban_stats'] = kanban_stats
        info['total_tasks'] = sum(kanban_stats.values())

        return info
    except Exception as e:
        print(f"Error reading feature {feature_path}: {e}")
        return None


def parse_tasks_markdown(tasks_file: Path) -> Dict[str, Any]:
    """
    Parse a single tasks.md file and extract tasks.

    Supports multiple task formats:
    1. Checkbox format: - [ ] T001 Description or - [x] T001 Description
    2. Header format: ### WP-001: Task Title or ### T001: Task Title
    3. Section-based: ## Planned / ## Doing / ## For Review / ## Done sections
    4. Phase-based (Normal mode): ## Phase 1: Name / ## Phase 2: Name sections

    Categorization priority:
    1. If task is under a lane section (## Planned, ## Doing, etc.) -> use that lane
    2. If task is under a phase section -> treat phases as lanes
    3. If checkbox is completed (- [x]) -> 'done'
    4. If checkbox is uncompleted (- [ ]) -> 'planned'
    5. Header tasks (###) -> 'planned' by default
    """
    import re

    lanes = {
        'planned': [],
        'doing': [],
        'for_review': [],
        'done': []
    }

    # Additional structure for phase-based tasks (Normal mode)
    phases = {}
    is_phase_mode = False

    try:
        with open(tasks_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # First, detect if this is a phase-based (Normal mode) file
        phase_pattern = re.compile(r'^## Phase (\d+):\s*(.+?)$', re.MULTILINE | re.IGNORECASE)
        phase_matches = list(phase_pattern.finditer(content))

        if phase_matches:
            # This is a Normal mode phase-based file
            is_phase_mode = True

            for i, phase_match in enumerate(phase_matches):
                phase_num = phase_match.group(1)
                phase_name = phase_match.group(2).strip()
                phase_start = phase_match.end()
                phase_end = phase_matches[i + 1].start() if i + 1 < len(phase_matches) else len(content)
                phase_content = content[phase_start:phase_end]

                # Determine phase status based on acceptance criteria checkboxes
                completed_criteria = len(re.findall(r'- \[[xX]\]', phase_content))
                total_criteria = len(re.findall(r'- \[[ xX]\]', phase_content))

                if completed_criteria == total_criteria and total_criteria > 0:
                    status = 'done'
                elif completed_criteria > 0:
                    status = 'doing'
                else:
                    # Check if previous phases are done
                    status = 'planned'

                phase_info = {
                    'id': f'Phase{phase_num}',
                    'title': f'Phase {phase_num}: {phase_name}',
                    'path': str(tasks_file),
                    'phase_num': int(phase_num),
                    'status': status,
                    'progress': f'{completed_criteria}/{total_criteria}' if total_criteria > 0 else '0/0'
                }

                phases[f'phase_{phase_num}'] = phase_info

                # Also add to appropriate lane for kanban compatibility
                lanes[status].append(phase_info)

            return {
                'lanes': lanes,
                'phases': phases,
                'mode': 'normal',
                'is_phase_mode': True
            }

        # Detect if file uses section-based organization
        # Look for ## headings that indicate lanes
        section_pattern = re.compile(r'^## (Planned|Doing|In Progress|For Review|Review|Done|Completed).*?$', re.MULTILINE | re.IGNORECASE)
        sections = list(section_pattern.finditer(content))

        if sections:
            # Section-based parsing
            current_lane = 'planned'

            # Split content by sections
            for i, section_match in enumerate(sections):
                section_name = section_match.group(1).lower()
                section_start = section_match.end()
                section_end = sections[i + 1].start() if i + 1 < len(sections) else len(content)
                section_content = content[section_start:section_end]

                # Map section names to lane names
                if 'doing' in section_name or 'progress' in section_name:
                    current_lane = 'doing'
                elif 'review' in section_name:
                    current_lane = 'for_review'
                elif 'done' in section_name or 'completed' in section_name:
                    current_lane = 'done'
                else:
                    current_lane = 'planned'

                # Parse tasks in this section
                # Checkbox tasks
                checkbox_pattern = re.compile(r'^- \[([ xX])\] ((?:T|WP-)\d+.*?)$', re.MULTILINE)
                for match in checkbox_pattern.finditer(section_content):
                    task_text = match.group(2).strip()
                    parts = task_text.split(' ', 1)
                    task_id = parts[0] if parts else task_text
                    task_title = parts[1] if len(parts) > 1 else task_text

                    lanes[current_lane].append({
                        'id': task_id,
                        'title': task_title,
                        'path': str(tasks_file)
                    })

                # Header tasks (supports T0.1, T1.1, WP-001, etc.)
                header_pattern = re.compile(r'^### ([A-Z]+-[\d.]+|T[\d.]+):\s*(.+?)$', re.MULTILINE)
                for match in header_pattern.finditer(section_content):
                    task_id = match.group(1).strip()
                    task_title = match.group(2).strip()

                    lanes[current_lane].append({
                        'id': task_id,
                        'title': task_title,
                        'path': str(tasks_file)
                    })
        else:
            # Non-section-based parsing (original behavior)
            # Pattern 1: Checkbox tasks
            checkbox_pattern = re.compile(r'^- \[([ xX])\] ((?:T|WP-)\d+.*?)$', re.MULTILINE)

            for match in checkbox_pattern.finditer(content):
                is_completed = match.group(1).lower() == 'x'
                task_text = match.group(2).strip()

                parts = task_text.split(' ', 1)
                task_id = parts[0] if parts else task_text
                task_title = parts[1] if len(parts) > 1 else task_text

                task_info = {
                    'id': task_id,
                    'title': task_title,
                    'path': str(tasks_file)
                }

                if is_completed:
                    lanes['done'].append(task_info)
                else:
                    lanes['planned'].append(task_info)

            # Pattern 2: Header tasks (supports T0.1, T1.1, WP-001, etc.)
            header_pattern = re.compile(r'^### ([A-Z]+-[\d.]+|T[\d.]+):\s*(.+?)$', re.MULTILINE)

            for match in header_pattern.finditer(content):
                task_id = match.group(1).strip()
                task_title = match.group(2).strip()

                task_info = {
                    'id': task_id,
                    'title': task_title,
                    'path': str(tasks_file)
                }

                lanes['planned'].append(task_info)

    except Exception as e:
        print(f"Error parsing tasks file {tasks_file}: {e}")

    return {'lanes': lanes, 'mode': 'pro', 'is_phase_mode': False}


def scan_feature_kanban(feature_id: str) -> Dict[str, Any]:
    """Scan kanban board for a feature"""
    # Try to find feature in specs/ or .worktrees/
    feature_path = None

    specs_path = Path('specs') / feature_id
    if specs_path.exists():
        feature_path = specs_path
    else:
        # Search in worktrees
        worktrees_dir = Path('.worktrees')
        if worktrees_dir.exists():
            for worktree_dir in worktrees_dir.iterdir():
                worktree_specs = worktree_dir / 'specs' / feature_id
                if worktree_specs.exists():
                    feature_path = worktree_specs
                    break

    if not feature_path:
        return {'error': 'Feature not found', 'lanes': {}}

    # First try: Check for directory-based kanban structure (tasks/{lane}/*.md)
    tasks_dir = feature_path / 'tasks'
    if tasks_dir.exists() and tasks_dir.is_dir():
        # Check if it contains lane subdirectories
        has_lane_dirs = any((tasks_dir / lane).exists() for lane in ['planned', 'doing', 'for_review', 'done'])

        if has_lane_dirs:
            lanes = {}
            for lane in ['planned', 'doing', 'for_review', 'done']:
                lane_dir = tasks_dir / lane
                lanes[lane] = []

                if lane_dir.exists():
                    for task_file in sorted(lane_dir.glob('*.md')):
                        task_info = {
                            'id': task_file.stem,
                            'title': task_file.stem,
                            'path': str(task_file)
                        }

                        # Try to extract title from file
                        try:
                            with open(task_file, 'r', encoding='utf-8') as f:
                                lines = f.readlines()
                                for line in lines:
                                    if line.startswith('# '):
                                        task_info['title'] = line.strip('# \n')
                                        break
                        except:
                            pass

                        lanes[lane].append(task_info)

            return {'lanes': lanes}

    # Second try: Parse single tasks.md file
    tasks_file = feature_path / 'tasks.md'
    if tasks_file.exists():
        return parse_tasks_markdown(tasks_file)

    # No tasks found
    return {'lanes': {'planned': [], 'doing': [], 'for_review': [], 'done': []}}


def get_artifact_content(feature_id: str, artifact_name: str) -> Optional[str]:
    """Get content of an artifact"""
    # Try to find feature
    feature_path = None

    specs_path = Path('specs') / feature_id
    if specs_path.exists():
        feature_path = specs_path
    else:
        worktrees_dir = Path('.worktrees')
        if worktrees_dir.exists():
            for worktree_dir in worktrees_dir.iterdir():
                worktree_specs = worktree_dir / 'specs' / feature_id
                if worktree_specs.exists():
                    feature_path = worktree_specs
                    break

    if not feature_path:
        return None

    artifact_path = feature_path / artifact_name
    if artifact_path.exists() and artifact_path.is_file():
        try:
            with open(artifact_path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return None

    return None


def get_task_detail(feature_id: str, lane: str, task_id: str) -> Optional[Dict[str, Any]]:
    """Get detailed information about a specific task"""
    import re
    import yaml

    # Try to find feature
    feature_path = None

    specs_path = Path('specs') / feature_id
    if specs_path.exists():
        feature_path = specs_path
    else:
        worktrees_dir = Path('.worktrees')
        if worktrees_dir.exists():
            for worktree_dir in worktrees_dir.iterdir():
                worktree_specs = worktree_dir / 'specs' / feature_id
                if worktree_specs.exists():
                    feature_path = worktree_specs
                    break

    if not feature_path:
        return None

    # Try 1: Work Package file in directory structure
    tasks_dir = feature_path / 'tasks'
    if tasks_dir.exists():
        task_file = tasks_dir / lane / f'{task_id}.md'
        if task_file.exists():
            try:
                with open(task_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract title and dependencies from frontmatter
                title = task_id
                dependencies = []
                lines = content.split('\n')

                # Try to extract from frontmatter
                if lines and lines[0].strip() == '---':
                    frontmatter_lines = []
                    end_index = 0
                    for i, line in enumerate(lines[1:], 1):
                        if line.strip() == '---':
                            end_index = i
                            break
                        frontmatter_lines.append(line)

                    if frontmatter_lines:
                        try:
                            frontmatter = yaml.safe_load('\n'.join(frontmatter_lines))
                            if frontmatter:
                                if 'title' in frontmatter:
                                    title = str(frontmatter['title'])
                                if 'dependencies' in frontmatter:
                                    deps = frontmatter['dependencies']
                                    if isinstance(deps, list):
                                        dependencies = deps
                                    elif isinstance(deps, str):
                                        # Parse comma-separated or space-separated
                                        dependencies = [d.strip() for d in re.split(r'[,\s]+', deps) if d.strip()]
                        except:
                            pass

                # If no frontmatter title, try first markdown heading
                if title == task_id:
                    for line in lines:
                        if line.startswith('# '):
                            title = line.strip('# \n')
                            break

                # Extract dependencies from content if not in frontmatter
                if not dependencies:
                    # Look for "Dependencies:", "Depends on:", "Requires:" sections
                    dep_pattern = re.compile(r'(?:Dependencies|Depends on|Requires):\s*(.+?)(?:\n\n|\Z)', re.IGNORECASE | re.DOTALL)
                    match = dep_pattern.search(content)
                    if match:
                        dep_text = match.group(1).strip()
                        # Extract task IDs (WP-XX, TXXXX, etc.)
                        task_id_pattern = re.compile(r'\b([A-Z]+-?\d+)\b')
                        dependencies = task_id_pattern.findall(dep_text)

                # Find lane for each dependency
                dependencies_with_lane = []
                for dep_id in dependencies:
                    dep_lane = find_task_lane(feature_path, dep_id)
                    dependencies_with_lane.append({
                        'id': dep_id,
                        'lane': dep_lane or 'planned'
                    })

                return {
                    'id': task_id,
                    'title': title,
                    'lane': lane,
                    'content': content,
                    'dependencies': dependencies_with_lane,
                    'path': str(task_file),
                    'type': 'work_package'
                }
            except Exception as e:
                print(f"Error reading task file {task_file}: {e}")
                return None

    # Try 2: Extract from tasks.md file
    tasks_file = feature_path / 'tasks.md'
    if tasks_file.exists():
        try:
            with open(tasks_file, 'r', encoding='utf-8') as f:
                content = f.read()

            dependencies = []

            # Find task section (### TASK_ID: or - [ ] TASK_ID)
            # Pattern 1: Header format (### WP-01: Task Title)
            header_pattern = re.compile(
                rf'^### ({re.escape(task_id)}):?\s*(.+?)$\n(.*?)(?=^### |^## |\Z)',
                re.MULTILINE | re.DOTALL
            )
            match = header_pattern.search(content)

            if match:
                title = match.group(2).strip()
                task_section = match.group(3).strip()
                task_content = f"# {task_id}: {title}\n\n{task_section}"

                # Extract dependencies from task section
                dep_pattern = re.compile(r'(?:Dependencies|Depends on|Requires):\s*(.+?)(?:\n\n|\Z)', re.IGNORECASE | re.DOTALL)
                dep_match = dep_pattern.search(task_section)
                if dep_match:
                    dep_text = dep_match.group(1).strip()
                    task_id_pattern = re.compile(r'\b([A-Z]+-?\d+)\b')
                    dependencies = task_id_pattern.findall(dep_text)

                # Find lane for each dependency
                dependencies_with_lane = []
                for dep_id in dependencies:
                    dep_lane = find_task_lane(feature_path, dep_id)
                    dependencies_with_lane.append({
                        'id': dep_id,
                        'lane': dep_lane or 'planned'
                    })

                return {
                    'id': task_id,
                    'title': title,
                    'lane': lane,
                    'content': task_content,
                    'dependencies': dependencies_with_lane,
                    'path': str(tasks_file),
                    'type': 'tasks_md'
                }

            # Pattern 2: Checkbox format (- [ ] TASK_ID Description)
            checkbox_pattern = re.compile(
                rf'^- \[([ xX])\] ({re.escape(task_id)})\s*(.*)$',
                re.MULTILINE
            )
            match = checkbox_pattern.search(content)

            if match:
                is_done = match.group(1).lower() == 'x'
                title = match.group(3).strip() or task_id
                task_content = f"# {task_id}\n\n{title}\n\n**Status**: {'Done' if is_done else 'Pending'}"

                return {
                    'id': task_id,
                    'title': title,
                    'lane': lane,
                    'content': task_content,
                    'dependencies': [],
                    'path': str(tasks_file),
                    'type': 'tasks_md'
                }

        except Exception as e:
            print(f"Error parsing tasks file {tasks_file}: {e}")
            return None

    return None


def find_task_lane(feature_path: Path, task_id: str) -> Optional[str]:
    """Find which lane a task is in"""
    tasks_dir = feature_path / 'tasks'

    if tasks_dir.exists() and tasks_dir.is_dir():
        # Check directory-based structure
        for lane in ['planned', 'doing', 'for_review', 'done']:
            lane_dir = tasks_dir / lane
            if lane_dir.exists():
                task_file = lane_dir / f'{task_id}.md'
                if task_file.exists():
                    return lane

    # Check tasks.md file
    tasks_file = feature_path / 'tasks.md'
    if tasks_file.exists():
        try:
            kanban_data = parse_tasks_markdown(tasks_file)
            for lane, tasks in kanban_data['lanes'].items():
                for task in tasks:
                    if task['id'] == task_id:
                        return lane
        except:
            pass

    return None


def get_task_commits(feature_id: str, task_id: str) -> List[Dict[str, Any]]:
    """
    Get git commits associated with a task.

    Args:
        feature_id: Feature ID (e.g., '001-feature-name')
        task_id: Task ID (e.g., 'WP01', 'WP01.1', 'T005')

    Returns:
        List of commits with sha, message, date, author
    """
    import subprocess

    # Check if git is available
    try:
        subprocess.run(['git', 'rev-parse', '--git-dir'],
                      capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []

    try:
        # Get commits that mention this task ID
        # Supports multiple formats:
        # - [WP04.3] Description (bracketed)
        # - feat: WP04.3 Description (conventional commits)
        # - WP04.3: Description (plain)
        import re
        escaped_task_id = re.escape(task_id)
        result = subprocess.run(
            ['git', 'log', '--all', f'--grep={escaped_task_id}',
             '--format=%H|%s|%cd|%an', '--date=iso-strict'],
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode != 0:
            return []

        commits = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue

            parts = line.split('|', 3)
            if len(parts) >= 4:
                sha, message, date, author = parts
                commits.append({
                    'sha': sha,
                    'short_sha': sha[:7],
                    'message': message,
                    'date': date,
                    'author': author
                })

        return commits
    except Exception as e:
        print(f"Error getting commits for task {task_id}: {e}")
        return []


def get_task_files(feature_id: str, task_id: str) -> List[Dict[str, Any]]:
    """
    Get files modified in commits associated with a task.

    Args:
        feature_id: Feature ID
        task_id: Task ID

    Returns:
        List of file changes with commit, path, action, timestamp
    """
    import subprocess

    commits = get_task_commits(feature_id, task_id)
    if not commits:
        return []

    file_changes = []

    for commit in commits:
        try:
            # Get files changed in this commit
            result = subprocess.run(
                ['git', 'show', '--name-status', '--format=', commit['sha']],
                capture_output=True,
                text=True,
                check=False
            )

            if result.returncode != 0:
                continue

            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue

                parts = line.split('\t', 1)
                if len(parts) >= 2:
                    status, path = parts
                    file_changes.append({
                        'commit': commit['short_sha'],
                        'commit_sha': commit['sha'],
                        'path': path,
                        'action': status,  # A=added, M=modified, D=deleted
                        'timestamp': commit['date'],
                        'message': commit['message']
                    })
        except Exception as e:
            print(f"Error getting files for commit {commit['sha']}: {e}")
            continue

    return file_changes


def get_commit_diff(commit_sha: str) -> Optional[str]:
    """
    Get the diff for a specific commit.

    Args:
        commit_sha: Full or short commit SHA

    Returns:
        Diff output as string, or None if error
    """
    import subprocess

    try:
        result = subprocess.run(
            ['git', 'show', commit_sha],
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode != 0:
            return None

        return result.stdout
    except Exception as e:
        print(f"Error getting diff for commit {commit_sha}: {e}")
        return None


def get_task_reviews(feature_id: str, task_id: str) -> List[Dict[str, Any]]:
    """
    Parse review history from a task's Activity Log.

    Args:
        feature_id: Feature ID (e.g., '001-feature-name')
        task_id: Task ID (e.g., 'WP01')

    Returns:
        List of review entries with timestamp, decision, reviewer, issues, and notes
    """
    # Find the task file
    specs_dir = Path('specs')
    feature_path = None

    # Try to find feature directory
    for spec_dir in specs_dir.glob('*'):
        if spec_dir.is_dir() and feature_id in spec_dir.name:
            feature_path = spec_dir
            break

    if not feature_path:
        return []

    # Search all lanes for the task file
    task_file = None
    current_lane = None
    tasks_dir = feature_path / 'tasks'

    if tasks_dir.exists():
        for lane in ['planned', 'doing', 'for_review', 'done']:
            lane_dir = tasks_dir / lane
            if lane_dir.exists():
                potential_file = lane_dir / f'{task_id}.md'
                if potential_file.exists():
                    task_file = potential_file
                    current_lane = lane
                    break

    if not task_file or not task_file.exists():
        return []

    # Parse the file for review entries
    reviews = []
    import re

    try:
        with open(task_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Look for [REVIEW] entries in Activity Log
        # Format: - {timestamp}: [REVIEW] {DECISION} by {reviewer}
        review_pattern = r'^- (.+?):\s*\[REVIEW\]\s+(APPROVED|CHANGES REQUESTED)\s+by\s+(.+?)$'

        in_activity_log = False
        current_review = None

        for line in content.split('\n'):
            # Detect Activity Log section (support multiple languages)
            line_stripped = line.strip()
            if (line_stripped.startswith('## Activity Log') or
                line_stripped.startswith('## 활동 로그') or
                line_stripped.startswith('## 작업 이력')):
                in_activity_log = True
                continue

            if in_activity_log:
                # Stop if we hit another section
                if line_stripped.startswith('##'):
                    break

                # Try to match review entry
                match = re.match(review_pattern, line.strip())
                if match:
                    timestamp, decision, reviewer = match.groups()

                    # Start a new review entry
                    if current_review and current_review not in reviews:
                        reviews.append(current_review)

                    current_review = {
                        'timestamp': timestamp.strip(),
                        'decision': decision.strip(),
                        'reviewer': reviewer.strip(),
                        'issues': [],
                        'positives': [],
                        'notes': []
                    }
                    continue

                # Parse sub-items (issues, positives, notes)
                if current_review and line.strip().startswith('- '):
                    # Remove leading "- "
                    item = line.strip()[2:].strip()

                    if item.startswith('❌'):
                        # Issue found
                        issue_text = item[1:].strip()
                        current_review['issues'].append(issue_text)
                    elif item.startswith('✅'):
                        # Positive point
                        positive_text = item[1:].strip()
                        current_review['positives'].append(positive_text)
                    elif item.startswith('Next steps:'):
                        # Next steps note
                        note_text = item[11:].strip()
                        current_review['notes'].append(note_text)
                    else:
                        # Generic note
                        current_review['notes'].append(item)

        # Add the last review if exists
        if current_review and current_review not in reviews:
            reviews.append(current_review)

    except Exception as e:
        print(f"Error parsing reviews from {task_file}: {e}")
        return []

    return reviews


def find_free_port(start_port: int = DEFAULT_PORT) -> int:
    """Find a free port starting from start_port"""
    import socket

    for port in range(start_port, start_port + MAX_PORT_ATTEMPTS):
        try:
            # Try to bind to the port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue

    raise RuntimeError(f"Could not find free port in range {start_port}-{start_port + MAX_PORT_ATTEMPTS}")


def start_dashboard(port: Optional[int] = None, open_browser: bool = False) -> tuple[HTTPServer, int, str]:
    """
    Start the dashboard server.

    Returns:
        Tuple of (server, port, shutdown_token)
    """
    if port is None:
        port = find_free_port()

    # Generate shutdown token
    shutdown_token = secrets.token_urlsafe(32)

    # Create server
    server = HTTPServer(('localhost', port), DashboardHandler)
    server.shutdown_token = shutdown_token

    # Save server info to .spec-mix/
    specify_dir = Path('.spec-mix')
    specify_dir.mkdir(exist_ok=True)

    (specify_dir / 'dashboard.pid').write_text(str(os.getpid()))
    (specify_dir / 'dashboard.port').write_text(str(port))
    (specify_dir / 'dashboard.token').write_text(shutdown_token)

    # Open browser if requested
    if open_browser:
        import webbrowser
        webbrowser.open(f'http://localhost:{port}')

    return server, port, shutdown_token


def stop_dashboard(port: Optional[int] = None):
    """Stop the dashboard server"""
    import httpx

    # Read port and token from .spec-mix/
    specify_dir = Path('.spec-mix')

    if port is None:
        port_file = specify_dir / 'dashboard.port'
        if port_file.exists():
            port = int(port_file.read_text().strip())
        else:
            port = DEFAULT_PORT

    token_file = specify_dir / 'dashboard.token'
    if token_file.exists():
        token = token_file.read_text().strip()
    else:
        print("No shutdown token found")
        return False

    # Send shutdown request
    try:
        response = httpx.post(
            f'http://localhost:{port}/api/shutdown',
            json={'token': token},
            timeout=5.0
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Error stopping dashboard: {e}")
        return False
    finally:
        # Cleanup files
        for file in [specify_dir / 'dashboard.pid',
                    specify_dir / 'dashboard.port',
                    specify_dir / 'dashboard.token']:
            if file.exists():
                file.unlink()


def get_untracked_commits(branch: str = 'HEAD', limit: int = 100) -> List[Dict[str, Any]]:
    """
    Get commits that don't have Work Package IDs.

    Args:
        branch: Git branch to analyze (default: HEAD)
        limit: Maximum number of commits to check

    Returns:
        List of commits without WP IDs, including sha, message, date, author, files, stats
    """
    import subprocess
    import re

    # Check if git is available
    try:
        subprocess.run(['git', 'rev-parse', '--git-dir'],
                      capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []

    # WP ID patterns to match
    # - WP04.3, WP04
    # - [WP04.3], [WP04]
    # - feat: WP04.3, fix: WP04
    wp_pattern = re.compile(r'\b(?:\[)?WP\d+(?:\.\d+)?(?:\])?', re.IGNORECASE)

    # Load migrated commits from .migration-info files
    migrated_commits = set()
    specs_dir = Path.cwd() / 'specs'
    if specs_dir.exists():
        for migration_file in specs_dir.glob('*/.migration-info'):
            try:
                with open(migration_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Try to parse as JSON first
                    try:
                        data = json.loads(content)
                        if 'migrated_commits' in data:
                            for sha in data['migrated_commits']:
                                migrated_commits.add(sha.lower()[:7])  # Short SHA
                                migrated_commits.add(sha.lower())  # Full SHA
                    except json.JSONDecodeError:
                        # Fallback: parse text format
                        in_commits_section = False
                        for line in content.split('\n'):
                            line = line.strip()
                            # Check for "Commits:" section header
                            if line.lower() == 'commits:':
                                in_commits_section = True
                                continue
                            # Parse commit list: "- abc1234: message"
                            if in_commits_section and line.startswith('- '):
                                parts = line[2:].split(':', 1)
                                if parts:
                                    sha = parts[0].strip()
                                    if sha and len(sha) >= 7:
                                        migrated_commits.add(sha.lower()[:7])
                                        migrated_commits.add(sha.lower())
                            # Also check for single commit format: "Migrated from commit: abc1234"
                            elif 'migrated from commit' in line.lower() and ':' in line:
                                sha = line.split(':')[-1].strip()
                                if sha:
                                    migrated_commits.add(sha.lower()[:7])
                                    migrated_commits.add(sha.lower())
            except Exception:
                pass

    try:
        # Get recent commits
        result = subprocess.run(
            ['git', 'log', branch, f'-{limit}',
             '--format=%H|%s|%cd|%an', '--date=iso-strict'],
            capture_output=True,
            text=True,
            check=False
        )

        if result.returncode != 0:
            return []

        untracked = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue

            parts = line.split('|', 3)
            if len(parts) < 4:
                continue

            sha, message, date, author = parts

            # Skip if message contains WP ID
            if wp_pattern.search(message):
                continue

            # Skip merge commits and automated commits
            if message.startswith('Merge') or '[skip ci]' in message:
                continue

            # Skip if commit was already migrated
            if sha.lower() in migrated_commits or sha.lower()[:7] in migrated_commits:
                continue

            # Get commit stats and files
            stat_result = subprocess.run(
                ['git', 'show', '--stat', '--format=', sha],
                capture_output=True,
                text=True,
                check=False
            )

            files_changed = []
            insertions = 0
            deletions = 0

            if stat_result.returncode == 0:
                for stat_line in stat_result.stdout.strip().split('\n'):
                    if '|' in stat_line:
                        # Parse file changes
                        file_part = stat_line.split('|')[0].strip()
                        if file_part:
                            files_changed.append(file_part)
                    elif 'file' in stat_line and 'changed' in stat_line:
                        # Parse summary line: "X files changed, Y insertions(+), Z deletions(-)"
                        matches = re.findall(r'(\d+)', stat_line)
                        if len(matches) >= 2:
                            insertions = int(matches[1]) if len(matches) > 1 else 0
                            deletions = int(matches[2]) if len(matches) > 2 else 0

            untracked.append({
                'sha': sha,
                'message': message,
                'date': date,
                'author': author,
                'files': files_changed,
                'stats': {
                    'insertions': insertions,
                    'deletions': deletions,
                    'files_changed': len(files_changed)
                }
            })

        return untracked

    except Exception as e:
        print(f"Error getting untracked commits: {e}")
        return []
