"""
Mode management commands for Specify CLI.

Provides commands to list, switch, and manage operational modes.
"""

import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .mode import get_mode_manager, MODES, InvalidModeError, ModeConfigError

console = Console()
mode_app = typer.Typer(
    name="mode",
    help="Manage operational mode for Spec Kit",
    add_completion=False,
)


@mode_app.command("list")
def list_modes():
    """List available operational modes."""
    try:
        manager = get_mode_manager()
        current_mode = manager.get_current_mode()
    except ModeConfigError:
        current_mode = None

    table = Table(title="Available Modes", show_header=True, header_style="bold cyan")
    table.add_column("Mode", style="cyan", width=12)
    table.add_column("Name", style="white", width=20)
    table.add_column("Description", style="dim")
    table.add_column("Status", style="green", width=10)

    for mode_key, mode_info in MODES.items():
        is_current = (mode_key == current_mode)
        status = "[cyan]Current[/cyan]" if is_current else ""
        table.add_row(mode_key, mode_info.name, mode_info.description, status)

    console.print()
    console.print(table)

    if current_mode:
        console.print()
        console.print(f"[cyan]Current mode:[/cyan] {MODES[current_mode].name} ({current_mode})")
    console.print()


@mode_app.command("current")
def show_current():
    """Show the currently active mode."""
    try:
        manager = get_mode_manager()
        current_mode = manager.get_current_mode()
        mode_info = manager.get_mode_info()

        console.print()
        console.print(f"[cyan]Current mode:[/cyan] {mode_info.name} ({current_mode})")
        console.print(f"[dim]{mode_info.description}[/dim]")
        console.print()
        console.print("[dim]To change mode:[/dim]")
        console.print("  specify mode set <mode>")
        console.print()
        console.print("[dim]To list available modes:[/dim]")
        console.print("  specify mode list")
        console.print()

    except ModeConfigError as e:
        console.print(f"[yellow]Warning:[/yellow] Could not read mode configuration: {e}")
        console.print(f"[cyan]Using default mode:[/cyan] pro")
        console.print()


@mode_app.command("set")
def set_mode(
    mode_key: str = typer.Argument(..., help="Mode to activate (normal or pro)"),
):
    """
    Set the active operational mode.

    Modes:
        normal - Simplified interface for streamlined workflows
        pro    - Full-featured interface with advanced commands

    Example:
        specify mode set normal
        specify mode set pro
    """
    try:
        manager = get_mode_manager()

        # Validate mode
        if mode_key not in MODES:
            available = ', '.join(MODES.keys())
            console.print(f"[red]Error:[/red] Invalid mode '{mode_key}'")
            console.print(f"[cyan]Available modes:[/cyan] {available}")
            console.print()
            console.print("[dim]Use 'specify mode list' to see all available modes[/dim]")
            raise typer.Exit(1)

        # Set the mode
        manager.set_mode(mode_key)
        mode_info = MODES[mode_key]

        console.print()
        console.print(f"[green]Mode switched to:[/green] {mode_info.name} ({mode_key})")
        console.print(f"[dim]{mode_info.description}[/dim]")
        console.print()

        # Mode-specific tips
        if mode_key == "normal":
            console.print("[cyan]Normal Mode Activated[/cyan]")
            console.print("Guided workflow with auto-clarify and phase-based implementation.")
            console.print()
            console.print("Start with [cyan]/spec-mix.specify[/cyan] to begin your project.")
            console.print()
        elif mode_key == "pro":
            console.print("[cyan]Pro Mode Activated[/cyan]")
            console.print("You now have access to all advanced commands:")
            console.print("  /spec-mix.constitution, /spec-mix.specify, /spec-mix.plan,")
            console.print("  /spec-mix.tasks, /spec-mix.implement, /spec-mix.clarify,")
            console.print("  /spec-mix.analyze, /spec-mix.checklist, /spec-mix.review,")
            console.print("  /spec-mix.accept, /spec-mix.merge, /spec-mix.dashboard")
            console.print()

    except InvalidModeError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    except ModeConfigError as e:
        console.print(f"[red]Error:[/red] Could not save mode configuration: {e}")
        console.print()
        console.print("[dim]Make sure you're in a Spec Kit project directory[/dim]")
        raise typer.Exit(1)


@mode_app.command("info")
def show_info(
    mode_key: str = typer.Argument(None, help="Mode to show info for (defaults to current)"),
):
    """
    Show detailed information about a mode.

    Example:
        specify mode info normal
        specify mode info pro
        specify mode info  # Show current mode info
    """
    try:
        manager = get_mode_manager()

        if mode_key is None:
            mode_key = manager.get_current_mode()
            is_current = True
        else:
            is_current = (mode_key == manager.get_current_mode())

        if mode_key not in MODES:
            available = ', '.join(MODES.keys())
            console.print(f"[red]Error:[/red] Invalid mode '{mode_key}'")
            console.print(f"[cyan]Available modes:[/cyan] {available}")
            raise typer.Exit(1)

        mode_info = MODES[mode_key]

        info_lines = [
            f"[bold cyan]{mode_info.name}[/bold cyan]",
            "",
            f"[white]Key:[/white] {mode_key}",
            f"[white]Description:[/white] {mode_info.description}",
        ]

        if is_current:
            info_lines.append("")
            info_lines.append("[green]Status:[/green] Currently Active")

        # Add mode-specific information
        if mode_key == "pro":
            info_lines.extend([
                "",
                "[bold]Available Commands:[/bold]",
                "  • /spec-mix.constitution - Establish project principles",
                "  • /spec-mix.specify - Create baseline specification",
                "  • /spec-mix.plan - Create implementation plan",
                "  • /spec-mix.tasks - Generate actionable tasks",
                "  • /spec-mix.implement - Execute implementation",
                "  • /spec-mix.clarify - Ask structured questions (optional)",
                "  • /spec-mix.analyze - Cross-artifact analysis (optional)",
                "  • /spec-mix.checklist - Generate quality checklists (optional)",
                "  • /spec-mix.review - Review completed tasks",
                "  • /spec-mix.accept - Final acceptance check",
                "  • /spec-mix.merge - Merge feature to main",
                "  • /spec-mix.dashboard - Web dashboard",
            ])
        elif mode_key == "normal":
            info_lines.extend([
                "",
                "[bold]Guided Workflow:[/bold]",
                "  1. /spec-mix.specify - Create spec with auto-clarify",
                "     → Automatically runs clarify questions",
                "     → Choose: Answer questions OR Skip to next step",
                "",
                "  2. /spec-mix.plan - Generate checklist + plan + tasks",
                "     → Tasks generated at phase level only",
                "",
                "  3. /spec-mix.implement - Execute phase by phase",
                "     → Walkthrough generated after each phase",
                "     → Review presented to user",
                "     → Accept/Reject choice for each phase",
                "",
                "  4. After completion: /spec-mix.merge to finalize",
                "",
                "[bold]Key Features:[/bold]",
                "  • Auto-clarify for better specifications",
                "  • Phase-based task management",
                "  • Built-in walkthrough and review",
                "  • Guided accept/reject workflow",
            ])

        panel = Panel(
            "\n".join(info_lines),
            title=f"Mode Information",
            border_style="cyan",
            padding=(1, 2)
        )

        console.print()
        console.print(panel)
        console.print()

    except ModeConfigError as e:
        console.print(f"[yellow]Warning:[/yellow] Could not read mode configuration: {e}")
        console.print(f"[cyan]Using default mode:[/cyan] pro")
        console.print()
