"""
Mode system for Spec Kit.

Modes determine the interface complexity and available commands:
- normal: Simplified interface for beginners
- pro: Full-featured interface with all advanced commands
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass


class ModeError(Exception):
    """Base exception for mode-related errors."""
    pass


class InvalidModeError(ModeError):
    """Raised when an invalid mode is specified."""
    pass


class ModeConfigError(ModeError):
    """Raised when mode configuration is invalid or inaccessible."""
    pass


@dataclass
class ModeInfo:
    """Information about a mode."""
    key: str
    name: str
    description: str


# Available modes configuration
MODES = {
    "normal": ModeInfo(
        key="normal",
        name="Normal Mode",
        description="Guided workflow with auto-clarify and phase-based implementation"
    ),
    "pro": ModeInfo(
        key="pro",
        name="Pro Mode",
        description="Full control with individual commands for each workflow step"
    )
}

DEFAULT_MODE = "normal"


class ModeManager:
    """
    Manages mode configuration and switching.
    """

    def __init__(self, project_dir: Optional[Path] = None):
        """
        Initialize mode manager.

        Args:
            project_dir: Path to project directory (default: current directory)
        """
        self.project_dir = project_dir or Path.cwd()
        self.config_dir = self.project_dir / '.spec-mix'
        self.config_file = self.config_dir / 'config.json'

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from config.json."""
        if not self.config_file.exists():
            return {}

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            raise ModeConfigError(f"Failed to load config: {e}")

    def _save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to config.json."""
        self.config_dir.mkdir(parents=True, exist_ok=True)

        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise ModeConfigError(f"Failed to save config: {e}")

    def get_current_mode(self) -> str:
        """
        Get the currently active mode.

        Returns:
            Current mode key (defaults to 'pro')
        """
        config = self._load_config()
        return config.get('mode', DEFAULT_MODE)

    def set_mode(self, mode_key: str) -> None:
        """
        Set the active mode.

        Args:
            mode_key: Mode key ('normal' or 'pro')

        Raises:
            InvalidModeError: If mode_key is not valid
        """
        if mode_key not in MODES:
            available = ', '.join(MODES.keys())
            raise InvalidModeError(f"Invalid mode '{mode_key}'. Available modes: {available}")

        config = self._load_config()
        config['mode'] = mode_key
        self._save_config(config)

    def get_mode_info(self, mode_key: Optional[str] = None) -> ModeInfo:
        """
        Get information about a specific mode or current mode.

        Args:
            mode_key: Mode key (defaults to current mode)

        Returns:
            ModeInfo for the specified mode

        Raises:
            InvalidModeError: If mode_key is not valid
        """
        if mode_key is None:
            mode_key = self.get_current_mode()

        if mode_key not in MODES:
            raise InvalidModeError(f"Invalid mode '{mode_key}'")

        return MODES[mode_key]

    def list_modes(self) -> Dict[str, ModeInfo]:
        """
        List all available modes.

        Returns:
            Dictionary mapping mode keys to ModeInfo objects
        """
        return MODES.copy()

    def is_pro_mode(self) -> bool:
        """
        Check if current mode is pro mode.

        Returns:
            True if in pro mode, False otherwise
        """
        return self.get_current_mode() == "pro"

    def is_normal_mode(self) -> bool:
        """
        Check if current mode is normal mode.

        Returns:
            True if in normal mode, False otherwise
        """
        return self.get_current_mode() == "normal"


def get_mode_manager(project_dir: Optional[Path] = None) -> ModeManager:
    """
    Get a mode manager instance.

    Args:
        project_dir: Path to project directory (default: current directory)

    Returns:
        ModeManager instance
    """
    return ModeManager(project_dir=project_dir)
