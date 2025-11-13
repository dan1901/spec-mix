"""
Mission system for Spec Kit.

Missions provide domain-specific templates, workflows, and validation rules
for different types of projects (software development, research, etc.).
"""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


class MissionError(Exception):
    """Base exception for mission-related errors."""
    pass


class MissionNotFoundError(MissionError):
    """Raised when a mission cannot be found."""
    pass


class MissionConfigError(MissionError):
    """Raised when mission configuration is invalid."""
    pass


@dataclass
class MissionMetadata:
    """Mission metadata from mission.yaml"""
    name: str
    description: str
    version: str
    domain: str


class Mission:
    """
    Represents a mission with its configuration, templates, and workflows.
    """

    def __init__(self, mission_path: Path):
        """
        Initialize a mission from a directory path.

        Args:
            mission_path: Path to mission directory containing mission.yaml
        """
        self.path = mission_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load and validate mission.yaml configuration."""
        config_path = self.path / "mission.yaml"

        if not config_path.exists():
            raise MissionConfigError(f"mission.yaml not found in {self.path}")

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise MissionConfigError(f"Invalid YAML in mission.yaml: {e}")

        # Validate required fields
        required_fields = ['name', 'description', 'version', 'domain']
        for field in required_fields:
            if field not in config:
                raise MissionConfigError(f"Missing required field: {field}")

        return config

    @property
    def metadata(self) -> MissionMetadata:
        """Get mission metadata."""
        return MissionMetadata(
            name=self.config['name'],
            description=self.config['description'],
            version=self.config['version'],
            domain=self.config['domain']
        )

    @property
    def name(self) -> str:
        """Get mission name."""
        return self.config['name']

    @property
    def description(self) -> str:
        """Get mission description."""
        return self.config['description']

    @property
    def version(self) -> str:
        """Get mission version."""
        return self.config['version']

    @property
    def domain(self) -> str:
        """Get mission domain."""
        return self.config['domain']

    def get_templates_dir(self) -> Optional[Path]:
        """Get path to mission templates directory."""
        templates_dir = self.config.get('directories', {}).get('templates', 'templates')
        path = self.path / templates_dir
        return path if path.exists() else None

    def get_commands_dir(self) -> Optional[Path]:
        """Get path to mission commands directory."""
        commands_dir = self.config.get('directories', {}).get('commands', 'commands')
        path = self.path / commands_dir
        return path if path.exists() else None

    def get_constitution_dir(self) -> Optional[Path]:
        """Get path to mission constitution directory."""
        constitution_dir = self.config.get('directories', {}).get('constitution', 'constitution')
        path = self.path / constitution_dir
        return path if path.exists() else None

    def list_templates(self) -> List[str]:
        """List available templates in this mission."""
        templates_dir = self.get_templates_dir()
        if not templates_dir:
            return []

        templates = []
        for file in templates_dir.glob('*.md'):
            templates.append(file.stem)
        return sorted(templates)

    def list_commands(self) -> List[str]:
        """List available commands in this mission."""
        commands_dir = self.get_commands_dir()
        if not commands_dir:
            return []

        commands = []
        for file in commands_dir.glob('*.md'):
            commands.append(file.stem)
        return sorted(commands)

    def get_workflow_phases(self) -> List[Dict[str, Any]]:
        """Get workflow phases configuration."""
        return self.config.get('workflow', {}).get('phases', [])

    def get_required_artifacts(self) -> List[str]:
        """Get list of required artifacts."""
        return self.config.get('artifacts', {}).get('required', [])

    def get_optional_artifacts(self) -> List[str]:
        """Get list of optional artifacts."""
        return self.config.get('artifacts', {}).get('optional', [])

    def get_validation_checks(self) -> List[str]:
        """Get list of validation check names."""
        return self.config.get('validation', {}).get('checks', [])

    def get_agent_context(self) -> Dict[str, str]:
        """Get agent personality and context configuration."""
        return self.config.get('agent_context', {})


class MissionManager:
    """
    Manages mission loading, switching, and discovery.
    """

    def __init__(self, locales_dir: Optional[Path] = None, locale: str = 'en'):
        """
        Initialize mission manager.

        Args:
            locales_dir: Path to locales directory (default: auto-detect)
            locale: Current locale (default: 'en')
        """
        if locales_dir is None:
            # Auto-detect locales directory
            pkg_root = Path(__file__).parent.parent.parent
            locales_dir = pkg_root / 'locales'

        self.locales_dir = locales_dir
        self.locale = locale
        self.missions_dir = locales_dir / locale / 'missions'

        # Fallback to .specify/missions for backward compatibility
        self.specify_missions_dir = Path('.specify') / 'missions'

    def get_missions_dir(self) -> Path:
        """Get the missions directory, preferring localized version."""
        if self.missions_dir.exists():
            return self.missions_dir
        elif self.specify_missions_dir.exists():
            return self.specify_missions_dir
        else:
            # Create localized missions directory
            self.missions_dir.mkdir(parents=True, exist_ok=True)
            return self.missions_dir

    def list_available_missions(self) -> List[str]:
        """
        List all available missions.

        Returns:
            List of mission directory names
        """
        missions_dir = self.get_missions_dir()
        missions = []

        for item in missions_dir.iterdir():
            if item.is_dir() and (item / 'mission.yaml').exists():
                missions.append(item.name)

        return sorted(missions)

    def get_mission(self, mission_name: str) -> Mission:
        """
        Load a mission by name.

        Args:
            mission_name: Name of the mission directory

        Returns:
            Mission instance

        Raises:
            MissionNotFoundError: If mission doesn't exist
        """
        missions_dir = self.get_missions_dir()
        mission_path = missions_dir / mission_name

        if not mission_path.exists():
            raise MissionNotFoundError(f"Mission not found: {mission_name}")

        return Mission(mission_path)

    def get_active_mission(self) -> str:
        """
        Get the currently active mission name.

        Returns:
            Name of active mission (defaults to 'software-dev')
        """
        # Check for active-mission marker in .specify/
        specify_dir = Path('.specify')
        active_mission_path = specify_dir / 'active-mission'

        # Try symlink first
        if active_mission_path.is_symlink():
            target = active_mission_path.readlink()
            # Extract mission name from path like 'missions/software-dev'
            return target.name

        # Try text file marker
        if active_mission_path.is_file():
            try:
                with open(active_mission_path, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            except Exception:
                pass

        # Default to software-dev
        return 'software-dev'

    def set_active_mission(self, mission_name: str) -> None:
        """
        Set the active mission.

        Args:
            mission_name: Name of the mission to activate

        Raises:
            MissionNotFoundError: If mission doesn't exist
        """
        # Validate mission exists
        _ = self.get_mission(mission_name)

        specify_dir = Path('.specify')
        specify_dir.mkdir(exist_ok=True)

        active_mission_path = specify_dir / 'active-mission'

        # Remove existing marker
        if active_mission_path.exists() or active_mission_path.is_symlink():
            active_mission_path.unlink()

        # Try to create symlink (portable)
        missions_dir = self.get_missions_dir()
        target_path = missions_dir / mission_name

        try:
            # Create relative symlink for portability
            rel_target = os.path.relpath(target_path, specify_dir)
            active_mission_path.symlink_to(rel_target)
        except (OSError, NotImplementedError):
            # Fallback to text file on systems without symlink support
            with open(active_mission_path, 'w', encoding='utf-8') as f:
                f.write(mission_name)

    def get_current_mission(self) -> Mission:
        """
        Get the currently active Mission instance.

        Returns:
            Mission instance for active mission
        """
        mission_name = self.get_active_mission()
        return self.get_mission(mission_name)


def get_mission_manager(locale: str = 'en') -> MissionManager:
    """
    Get a mission manager instance.

    Args:
        locale: Locale to use for mission loading

    Returns:
        MissionManager instance
    """
    return MissionManager(locale=locale)
