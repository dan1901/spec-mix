
import os
import json
import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server

from .dashboard import (
    scan_all_features,
    get_feature_info,
    get_artifact_content,
    scan_feature_kanban,
    get_task_detail
)

# Initialize server
server = Server("spec-mix-mcp")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="get_project_context",
            description="Get the current project context, including active features and their status.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        types.Tool(
            name="read_plan",
            description="Read the implementation plan for a specific feature.",
            inputSchema={
                "type": "object",
                "properties": {
                    "feature_id": {
                        "type": "string",
                        "description": "ID of the feature to read plan for (e.g. 'feature-001'). If omitted, tries to find the active feature.",
                    },
                },
            },
        ),
        types.Tool(
            name="update_plan",
            description="Update the implementation plan for a feature.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "New content for the plan.md file.",
                    },
                    "feature_id": {
                        "type": "string",
                        "description": "ID of the feature. If omitted, tries to find the active feature.",
                    },
                },
                "required": ["content"],
            },
        ),
        types.Tool(
            name="list_tasks",
            description="List all tasks in the kanban board for a feature.",
            inputSchema={
                "type": "object",
                "properties": {
                    "feature_id": {
                        "type": "string",
                        "description": "ID of the feature. If omitted, tries to find the active feature.",
                    },
                },
            },
        ),
        types.Tool(
            name="create_task",
            description="Create a new task in the 'Planned' lane.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Title of the task.",
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed description of the task.",
                    },
                    "feature_id": {
                        "type": "string",
                        "description": "ID of the feature. If omitted, tries to find the active feature.",
                    },
                },
                "required": ["title", "description"],
            },
        ),
        types.Tool(
            name="update_task_status",
            description="Move a task to a different lane (planned, doing, for_review, done).",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "ID of the task to move.",
                    },
                    "lane": {
                        "type": "string",
                        "enum": ["planned", "doing", "for_review", "done"],
                        "description": "Target lane.",
                    },
                    "feature_id": {
                        "type": "string",
                        "description": "ID of the feature. If omitted, tries to find the active feature.",
                    },
                },
                "required": ["task_id", "lane"],
            },
        ),
    ]

def _get_active_feature_id() -> Optional[str]:
    """Try to determine the active feature ID from environment or context."""
    # Check env var
    if os.environ.get("SPECIFY_FEATURE"):
        return os.environ.get("SPECIFY_FEATURE")
    
    # Check if we are in a feature directory
    cwd = Path.cwd()
    if (cwd / "specs").exists():
        # We are at root, maybe check .spec-mix/active-mission/context.json if it exists?
        # For now, return the first feature found if any
        features = scan_all_features()
        if features:
            return features[0]['id']
            
    return None

def _resolve_feature_path(feature_id: Optional[str]) -> Optional[Path]:
    """Resolve feature ID to a path."""
    if not feature_id:
        feature_id = _get_active_feature_id()
    
    if not feature_id:
        return None
        
    # Check specs/
    specs_path = Path('specs') / feature_id
    if specs_path.exists():
        return specs_path
        
    # Check worktrees
    worktrees_dir = Path('.worktrees')
    if worktrees_dir.exists():
        for worktree_dir in worktrees_dir.iterdir():
            worktree_specs = worktree_dir / 'specs' / feature_id
            if worktree_specs.exists():
                return worktree_specs
                
    return None

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution."""
    if not arguments:
        arguments = {}

    if name == "get_project_context":
        features = scan_all_features()
        return [types.TextContent(type="text", text=json.dumps(features, indent=2))]

    elif name == "read_plan":
        feature_id = arguments.get("feature_id")
        if not feature_id:
            feature_id = _get_active_feature_id()
            
        if not feature_id:
            return [types.TextContent(type="text", text="Error: No active feature found and no feature_id provided.")]
            
        content = get_artifact_content(feature_id, "plan.md")
        if content:
            return [types.TextContent(type="text", text=content)]
        else:
            return [types.TextContent(type="text", text=f"Error: plan.md not found for feature {feature_id}")]

    elif name == "update_plan":
        feature_id = arguments.get("feature_id")
        content = arguments.get("content")
        
        path = _resolve_feature_path(feature_id)
        if not path:
             return [types.TextContent(type="text", text=f"Error: Feature {feature_id} not found.")]
             
        plan_path = path / "plan.md"
        try:
            with open(plan_path, "w", encoding="utf-8") as f:
                f.write(content)
            return [types.TextContent(type="text", text=f"Successfully updated plan.md for {path.name}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error updating plan: {str(e)}")]

    elif name == "list_tasks":
        feature_id = arguments.get("feature_id")
        if not feature_id:
            feature_id = _get_active_feature_id()
            
        if not feature_id:
            return [types.TextContent(type="text", text="Error: No active feature found and no feature_id provided.")]
            
        kanban = scan_feature_kanban(feature_id)
        return [types.TextContent(type="text", text=json.dumps(kanban, indent=2))]

    elif name == "create_task":
        feature_id = arguments.get("feature_id")
        title = arguments.get("title")
        description = arguments.get("description")
        
        path = _resolve_feature_path(feature_id)
        if not path:
             return [types.TextContent(type="text", text=f"Error: Feature {feature_id} not found.")]
             
        # Determine task ID (simple auto-increment for now, or random)
        # Ideally we should scan existing tasks to find max ID
        # For simplicity, let's use a timestamp or random ID if we can't easily determine next ID
        # Or better, check existing tasks count
        kanban = scan_feature_kanban(path.name)
        total_tasks = 0
        for lane in kanban.get('lanes', {}).values():
            total_tasks += len(lane)
        
        # Simple ID generation: T{total_tasks + 1}
        task_id = f"T{total_tasks + 1:03d}"
        
        # Check if directory based or file based
        tasks_dir = path / "tasks"
        if tasks_dir.exists() and tasks_dir.is_dir():
            # Directory based
            planned_dir = tasks_dir / "planned"
            planned_dir.mkdir(exist_ok=True)
            
            task_file = planned_dir / f"{task_id}.md"
            content = f"---\ntitle: {title}\nstatus: planned\n---\n\n# {task_id}: {title}\n\n{description}"
            
            with open(task_file, "w", encoding="utf-8") as f:
                f.write(content)
                
        else:
            # File based (tasks.md)
            tasks_file = path / "tasks.md"
            # Append to tasks.md
            # We need to read it, find "## Planned" section and insert
            # Or just append if simple format
            # For safety, let's just append to the end or create if not exists
            
            task_entry = f"\n\n### {task_id}: {title}\n{description}\n"
            
            if tasks_file.exists():
                with open(tasks_file, "a", encoding="utf-8") as f:
                    f.write(task_entry)
            else:
                with open(tasks_file, "w", encoding="utf-8") as f:
                    f.write(f"# Tasks\n\n## Planned{task_entry}\n\n## Doing\n\n## For Review\n\n## Done\n")
                    
        return [types.TextContent(type="text", text=f"Created task {task_id}: {title}")]

    elif name == "update_task_status":
        task_id = arguments.get("task_id")
        lane = arguments.get("lane")
        feature_id = arguments.get("feature_id")
        
        path = _resolve_feature_path(feature_id)
        if not path:
             return [types.TextContent(type="text", text=f"Error: Feature {feature_id} not found.")]
             
        # Check if directory based
        tasks_dir = path / "tasks"
        if tasks_dir.exists() and tasks_dir.is_dir():
            # Move file
            found_file = None
            for l in ["planned", "doing", "for_review", "done"]:
                l_dir = tasks_dir / l
                if (l_dir / f"{task_id}.md").exists():
                    found_file = l_dir / f"{task_id}.md"
                    break
            
            if found_file:
                target_dir = tasks_dir / lane
                target_dir.mkdir(exist_ok=True)
                target_file = target_dir / f"{task_id}.md"
                found_file.rename(target_file)
                return [types.TextContent(type="text", text=f"Moved task {task_id} to {lane}")]
            else:
                 return [types.TextContent(type="text", text=f"Error: Task {task_id} not found.")]
        else:
            # File based - complex to update safely without parsing
            # For now, return error for file-based update as it requires robust parsing/rewriting
            return [types.TextContent(type="text", text="Error: Updating task status in tasks.md file is not yet supported via MCP. Please use directory-based tasks.")]

    raise ValueError(f"Unknown tool: {name}")

async def run():
    # Run the server using stdin/stdout streams
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="spec-mix-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    import sys
    print("Spec Mix MCP server running on stdio...", file=sys.stderr)
    asyncio.run(run())
