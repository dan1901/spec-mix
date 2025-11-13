"""
CLI commands for mission management.
"""

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from pathlib import Path
from typing import Optional

from .mission import MissionManager, MissionNotFoundError, MissionError

try:
    from .i18n import get_locale_manager, t
    HAS_I18N = True
except ImportError:
    HAS_I18N = False
    def t(key, **kwargs):
        return key


mission_app = typer.Typer(
    name="mission",
    help="Manage missions for different project types"
)
console = Console()


@mission_app.command("list")
def list_missions():
    """List all available missions."""
    if HAS_I18N:
        from .i18n import init_i18n
        init_i18n()
        locale = get_locale_manager().current_locale
    else:
        locale = 'en'
    manager = MissionManager(locale=locale)

    try:
        missions = manager.list_available_missions()
        active_mission = manager.get_active_mission()

        if not missions:
            console.print("[yellow]No missions found.[/yellow]")
            return

        # Create table
        table = Table(title=t("cli.mission.list_header", default="Available Missions"))
        table.add_column("Mission", style="cyan")
        table.add_column("Name", style="white")
        table.add_column("Description", style="dim")
        table.add_column("Active", style="green")

        for mission_name in missions:
            try:
                mission = manager.get_mission(mission_name)
                is_active = "✓" if mission_name == active_mission else ""

                table.add_row(
                    mission_name,
                    mission.name,
                    mission.description,
                    is_active
                )
            except MissionError as e:
                console.print(f"[red]Error loading mission {mission_name}: {e}[/red]")

        console.print(table)

        # Show active mission info
        console.print(f"\n[green]✓[/green] {t('cli.mission.current_mission', default='Current mission: {mission}', mission=active_mission)}")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@mission_app.command("current")
def current_mission():
    """Show information about the currently active mission."""
    if HAS_I18N:
        from .i18n import init_i18n
        init_i18n()
        locale = get_locale_manager().current_locale
    else:
        locale = 'en'
    manager = MissionManager(locale=locale)

    try:
        mission = manager.get_current_mission()

        # Create info panel
        info_lines = [
            f"**Name:** {mission.name}",
            f"**Description:** {mission.description}",
            f"**Version:** {mission.version}",
            f"**Domain:** {mission.domain}",
        ]

        # Add templates info
        templates = mission.list_templates()
        if templates:
            info_lines.append(f"\n**Templates:** {', '.join(templates)}")

        # Add commands info
        commands = mission.list_commands()
        if commands:
            info_lines.append(f"**Commands:** {', '.join(commands)}")

        # Add workflow phases
        phases = mission.get_workflow_phases()
        if phases:
            phase_names = [p.get('name', 'Unknown') for p in phases]
            info_lines.append(f"\n**Workflow Phases:** {' → '.join(phase_names)}")

        # Add artifacts info
        required = mission.get_required_artifacts()
        optional = mission.get_optional_artifacts()
        if required:
            info_lines.append(f"\n**Required Artifacts:** {', '.join(required)}")
        if optional:
            info_lines.append(f"**Optional Artifacts:** {', '.join(optional)}")

        info_text = "\n".join(info_lines)

        console.print(Panel(
            info_text,
            title=t("cli.mission.mission_info", default="Mission Information"),
            border_style="green"
        ))

    except MissionNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        raise typer.Exit(1)


@mission_app.command("switch")
def switch_mission(
    mission_name: str = typer.Argument(..., help="Name of the mission to activate")
):
    """Switch to a different mission."""
    if HAS_I18N:
        from .i18n import init_i18n
        init_i18n()
        locale = get_locale_manager().current_locale
    else:
        locale = 'en'
    manager = MissionManager(locale=locale)

    try:
        # Validate mission exists
        mission = manager.get_mission(mission_name)

        # Set as active
        manager.set_active_mission(mission_name)

        console.print(f"[green]✓[/green] {t('cli.mission.switched_to', default='Switched to mission: {mission}', mission=mission.name)}")
        console.print(f"\n[dim]Templates and commands will now use the {mission.name} mission configuration.[/dim]")

    except MissionNotFoundError:
        console.print(f"[red]✗[/red] {t('cli.mission.not_found', default='Mission not found: {mission}', mission=mission_name)}")
        console.print("\n[dim]Available missions:[/dim]")
        list_missions()
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@mission_app.command("info")
def mission_info(
    mission_name: str = typer.Argument(..., help="Name of the mission to inspect")
):
    """Show detailed information about a specific mission."""
    if HAS_I18N:
        from .i18n import init_i18n
        init_i18n()
        locale = get_locale_manager().current_locale
    else:
        locale = 'en'
    manager = MissionManager(locale=locale)

    try:
        mission = manager.get_mission(mission_name)
        active_mission = manager.get_active_mission()
        is_active = mission_name == active_mission

        # Build info display
        info_lines = [
            f"# {mission.name}",
            f"\n{mission.description}",
            f"\n**Version:** {mission.version}",
            f"**Domain:** {mission.domain}",
            f"**Status:** {'✓ Active' if is_active else 'Available'}",
        ]

        # Directories
        info_lines.append("\n## Directories")
        templates_dir = mission.get_templates_dir()
        commands_dir = mission.get_commands_dir()
        constitution_dir = mission.get_constitution_dir()

        if templates_dir:
            info_lines.append(f"- Templates: `{templates_dir}`")
        if commands_dir:
            info_lines.append(f"- Commands: `{commands_dir}`")
        if constitution_dir:
            info_lines.append(f"- Constitution: `{constitution_dir}`")

        # Templates
        templates = mission.list_templates()
        if templates:
            info_lines.append("\n## Templates")
            for template in templates:
                info_lines.append(f"- {template}")

        # Commands
        commands = mission.list_commands()
        if commands:
            info_lines.append("\n## Commands")
            for command in commands:
                info_lines.append(f"- /speckit.{command}")

        # Workflow
        phases = mission.get_workflow_phases()
        if phases:
            info_lines.append("\n## Workflow Phases")
            for phase in phases:
                name = phase.get('name', 'Unknown')
                required = phase.get('required', False)
                status = "Required" if required else "Optional"
                info_lines.append(f"- **{name}** ({status})")

        # Artifacts
        required_artifacts = mission.get_required_artifacts()
        optional_artifacts = mission.get_optional_artifacts()

        if required_artifacts or optional_artifacts:
            info_lines.append("\n## Artifacts")
            if required_artifacts:
                info_lines.append("\n**Required:**")
                for artifact in required_artifacts:
                    info_lines.append(f"- {artifact}")
            if optional_artifacts:
                info_lines.append("\n**Optional:**")
                for artifact in optional_artifacts:
                    info_lines.append(f"- {artifact}")

        # Validation
        checks = mission.get_validation_checks()
        if checks:
            info_lines.append("\n## Validation Checks")
            for check in checks:
                info_lines.append(f"- {check}")

        # Agent context
        agent_context = mission.get_agent_context()
        if agent_context:
            info_lines.append("\n## Agent Context")
            if 'personality' in agent_context:
                info_lines.append(f"**Personality:** {agent_context['personality']}")
            if 'focus' in agent_context:
                info_lines.append(f"**Focus:** {agent_context['focus']}")

        # Render as markdown
        md = Markdown("\n".join(info_lines))
        console.print(md)

    except MissionNotFoundError:
        console.print(f"[red]✗[/red] {t('cli.mission.not_found', default='Mission not found: {mission}', mission=mission_name)}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    mission_app()
