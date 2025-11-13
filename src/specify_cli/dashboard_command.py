"""
CLI commands for dashboard management.
"""

import typer
import sys
from rich.console import Console
from pathlib import Path
from typing import Optional

from .dashboard import start_dashboard, stop_dashboard, DEFAULT_PORT

console = Console()

dashboard_app = typer.Typer(
    name="dashboard",
    help="Start and manage the Spec Kit dashboard"
)


@dashboard_app.command("start")
def start(
    port: Optional[int] = typer.Option(None, "--port", "-p", help=f"Port to run dashboard on (default: {DEFAULT_PORT})"),
    open_browser: bool = typer.Option(False, "--open", "-o", help="Open dashboard in browser"),
    detach: bool = typer.Option(False, "--detach", "-d", help="Run dashboard in background")
):
    """Start the dashboard server."""
    try:
        if detach:
            console.print("[yellow]Background mode not yet implemented. Running in foreground...[/yellow]")

        server, actual_port, token = start_dashboard(port=port, open_browser=open_browser)

        console.print(f"[green]✓[/green] Dashboard started successfully!")
        console.print(f"\n[cyan]URL:[/cyan] http://localhost:{actual_port}")
        console.print(f"[dim]Shutdown token saved to .specify/dashboard.token[/dim]")
        console.print(f"\n[yellow]Press Ctrl+C to stop the dashboard[/yellow]\n")

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            console.print("\n[yellow]Shutting down dashboard...[/yellow]")
            server.shutdown()
            console.print("[green]✓[/green] Dashboard stopped")

    except Exception as e:
        console.print(f"[red]Error starting dashboard: {e}[/red]")
        raise typer.Exit(1)


@dashboard_app.command("stop")
def stop(
    port: Optional[int] = typer.Option(None, "--port", "-p", help="Port dashboard is running on")
):
    """Stop the dashboard server."""
    try:
        success = stop_dashboard(port=port)

        if success:
            console.print("[green]✓[/green] Dashboard stopped successfully")
        else:
            console.print("[yellow]Dashboard may not be running or failed to stop[/yellow]")

    except Exception as e:
        console.print(f"[red]Error stopping dashboard: {e}[/red]")
        raise typer.Exit(1)


@dashboard_app.command("status")
def status():
    """Check dashboard status."""
    specify_dir = Path('.specify')
    pid_file = specify_dir / 'dashboard.pid'
    port_file = specify_dir / 'dashboard.port'

    if pid_file.exists() and port_file.exists():
        pid = pid_file.read_text().strip()
        port = port_file.read_text().strip()

        console.print(f"[green]✓[/green] Dashboard appears to be running")
        console.print(f"  PID: {pid}")
        console.print(f"  Port: {port}")
        console.print(f"  URL: http://localhost:{port}")
    else:
        console.print("[yellow]Dashboard is not running[/yellow]")


@dashboard_app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Manage the Spec Kit dashboard.

    If no subcommand is provided, starts the dashboard.
    """
    if ctx.invoked_subcommand is None:
        # Default action: start dashboard
        start(port=None, open_browser=True, detach=False)


if __name__ == "__main__":
    dashboard_app()
