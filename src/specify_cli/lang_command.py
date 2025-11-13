"""
Language management commands for Specify CLI.

Provides commands to list, install, and manage language packs.
"""

import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .i18n import get_locale_manager

console = Console()
lang_app = typer.Typer(
    name="lang",
    help="Manage language packs for Specify",
    add_completion=False,
)


def get_locales_dir() -> Path:
    """Get the locales directory path."""
    pkg_root = Path(__file__).parent.parent.parent
    return pkg_root / "locales"


@lang_app.command("list")
def list_languages():
    """List available and installed languages."""
    lm = get_locale_manager()
    installed = set(lm.get_installed_locales())
    supported = lm.get_supported_locales()

    table = Table(title="Available Languages", show_header=True, header_style="bold cyan")
    table.add_column("Code", style="cyan", width=8)
    table.add_column("Name", style="white")
    table.add_column("Status", style="green")

    for locale_info in supported:
        code = locale_info['code']
        name = f"{locale_info['native_name']} ({locale_info['name']})"
        is_default = locale_info.get('is_default', False)
        is_current = (code == lm.current_locale)

        status_parts = []
        if code in installed:
            status_parts.append("[green]Installed[/green]")
        if is_default:
            status_parts.append("[yellow]Default[/yellow]")
        if is_current:
            status_parts.append("[cyan]Current[/cyan]")

        status = ", ".join(status_parts) if status_parts else "[dim]Available[/dim]"
        table.add_row(code, name, status)

    console.print()
    console.print(table)
    console.print()
    console.print(f"[cyan]Current language:[/cyan] {lm.get_locale_name(lm.current_locale)}")
    console.print()


@lang_app.command("install")
def install_language(
    locale_code: str = typer.Argument(..., help="Language code to install (e.g., ko, ja, fr)"),
    github_token: str = typer.Option(None, "--github-token", help="GitHub token for API requests"),
):
    """
    Install a language pack from the latest Specify release.

    Example:
        specify lang install ko
    """
    lm = get_locale_manager()

    # Check if already installed
    if locale_code in lm.get_installed_locales():
        console.print(f"[yellow]Language pack '{locale_code}' is already installed[/yellow]")
        return

    # Check if locale is supported
    supported_codes = [loc['code'] for loc in lm.get_supported_locales()]
    if locale_code not in supported_codes:
        console.print(f"[red]Language '{locale_code}' is not available[/red]")
        console.print(f"[cyan]Supported languages:[/cyan] {', '.join(supported_codes)}")
        raise typer.Exit(1)

    console.print(f"[cyan]Installing language pack:[/cyan] {locale_code}")
    console.print("[dim]Downloading from GitHub releases...[/dim]")

    # Download language pack from GitHub releases
    # For now, we'll create a placeholder since we need to set up the release structure
    console.print()
    console.print(Panel(
        "[yellow]Language pack installation from GitHub releases is not yet implemented.[/yellow]\n\n"
        "For now, language packs are bundled with the main package.\n"
        "This feature will be available in a future release.",
        title="[yellow]Feature Coming Soon[/yellow]",
        border_style="yellow"
    ))


@lang_app.command("set")
def set_language(
    locale_code: str = typer.Argument(..., help="Language code to set as default (e.g., ko)"),
):
    """
    Set the default language for Specify CLI.

    This sets the SPECIFY_LANG environment variable for future sessions.

    Example:
        specify lang set ko
    """
    lm = get_locale_manager()

    # Check if locale is installed
    if locale_code not in lm.get_installed_locales():
        console.print(f"[red]Language '{locale_code}' is not installed[/red]")
        console.print(f"[cyan]Install it first with:[/cyan] specify lang install {locale_code}")
        raise typer.Exit(1)

    # Set the locale
    if lm.set_locale(locale_code):
        console.print(f"[green]Default language set to:[/green] {lm.get_locale_name(locale_code)}")
        console.print()
        console.print("[cyan]To make this permanent, add to your shell profile:[/cyan]")
        console.print(f"  export SPECIFY_LANG={locale_code}")
    else:
        console.print(f"[red]Failed to set language to '{locale_code}'[/red]")
        raise typer.Exit(1)


@lang_app.command("current")
def show_current():
    """Show the currently active language."""
    lm = get_locale_manager()
    console.print()
    console.print(f"[cyan]Current language:[/cyan] {lm.get_locale_name(lm.current_locale)} ({lm.current_locale})")
    console.print()
    console.print("[dim]To change language:[/dim]")
    console.print("  specify lang set <code>")
    console.print()
    console.print("[dim]To list available languages:[/dim]")
    console.print("  specify lang list")
    console.print()
