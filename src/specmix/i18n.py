"""
Internationalization (i18n) support for Specify CLI.

Provides locale detection, string loading, and translation utilities.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
import locale as system_locale


class LocaleManager:
    """Manages localization for Specify CLI."""

    def __init__(self, locales_dir: Optional[Path] = None):
        """
        Initialize the LocaleManager.

        Args:
            locales_dir: Path to locales directory. If None, uses package default.
        """
        if locales_dir is None:
            # Use locales directory relative to this file
            # locales is in src/specmix/locales/
            locales_dir = Path(__file__).parent / "locales"

        self.locales_dir = locales_dir
        self.config = self._load_config()
        self.current_locale = self._detect_locale()
        self.strings: Dict[str, Any] = {}
        self._load_strings()

    def _load_config(self) -> Dict[str, Any]:
        """Load locale configuration."""
        config_file = self.locales_dir / "config.json"
        if not config_file.exists():
            return {
                "default_locale": "en",
                "supported_locales": [{"code": "en", "name": "English", "native_name": "English", "is_default": True}],
                "fallback_locale": "en"
            }

        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _detect_locale(self) -> str:
        """
        Detect locale from environment or system settings.

        Priority:
        1. SPECIFY_LANG environment variable
        2. System locale (LANG, LC_ALL)
        3. Default locale from config
        """
        # Check environment variable
        env_lang = os.environ.get('SPECIFY_LANG')
        if env_lang and self._is_locale_available(env_lang):
            return env_lang

        # Check system locale
        try:
            sys_locale, _ = system_locale.getdefaultlocale()
            if sys_locale:
                # Extract language code (e.g., 'ko_KR' -> 'ko')
                lang_code = sys_locale.split('_')[0]
                if self._is_locale_available(lang_code):
                    return lang_code
        except Exception:
            pass

        # Fall back to default
        return self.config.get('default_locale', 'en')

    def _is_locale_available(self, locale_code: str) -> bool:
        """Check if a locale is available (has strings file)."""
        strings_file = self.locales_dir / locale_code / "strings.json"
        return strings_file.exists()

    def _load_strings(self) -> None:
        """Load strings for current locale with fallback."""
        strings_file = self.locales_dir / self.current_locale / "strings.json"
        fallback_locale = self.config.get('fallback_locale', 'en')
        fallback_file = self.locales_dir / fallback_locale / "strings.json"

        # Load fallback first
        if fallback_file.exists() and self.current_locale != fallback_locale:
            with open(fallback_file, 'r', encoding='utf-8') as f:
                self.strings = json.load(f)

        # Override with current locale
        if strings_file.exists():
            with open(strings_file, 'r', encoding='utf-8') as f:
                current_strings = json.load(f)
                self._deep_merge(self.strings, current_strings)
        elif self.current_locale != fallback_locale:
            # If current locale not found, fall back completely
            self.current_locale = fallback_locale

    def _deep_merge(self, base: Dict, update: Dict) -> None:
        """Deep merge update dict into base dict (in-place)."""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value

    def get(self, key_path: str, **kwargs) -> str:
        """
        Get localized string by dot-notation key path.

        Args:
            key_path: Dot-separated path like 'cli.init.project_ready'
            **kwargs: Format arguments for the string

        Returns:
            Localized string with format arguments applied
        """
        keys = key_path.split('.')
        value = self.strings

        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
                if value is None:
                    return f"[MISSING: {key_path}]"
            else:
                return f"[INVALID PATH: {key_path}]"

        if isinstance(value, str):
            try:
                return value.format(**kwargs)
            except KeyError as e:
                return f"[FORMAT ERROR in {key_path}: missing {e}]"

        return f"[NOT A STRING: {key_path}]"

    def get_supported_locales(self) -> list:
        """Get list of supported locales from config."""
        return self.config.get('supported_locales', [])

    def get_installed_locales(self) -> list:
        """Get list of installed locale codes."""
        if not self.locales_dir.exists():
            return []

        installed = []
        for item in self.locales_dir.iterdir():
            if item.is_dir() and (item / "strings.json").exists():
                installed.append(item.name)

        return installed

    def set_locale(self, locale_code: str) -> bool:
        """
        Set current locale.

        Args:
            locale_code: Locale code to set

        Returns:
            True if successful, False if locale not available
        """
        if not self._is_locale_available(locale_code):
            return False

        self.current_locale = locale_code
        self.strings = {}
        self._load_strings()
        return True

    def get_locale_name(self, locale_code: str) -> str:
        """Get display name for a locale code."""
        for loc in self.get_supported_locales():
            if loc['code'] == locale_code:
                return f"{loc['native_name']} ({loc['name']})"
        return locale_code


# Global instance
_locale_manager: Optional[LocaleManager] = None


def init_i18n(locales_dir: Optional[Path] = None) -> LocaleManager:
    """Initialize the global locale manager."""
    global _locale_manager
    _locale_manager = LocaleManager(locales_dir)
    return _locale_manager


def get_locale_manager() -> LocaleManager:
    """Get the global locale manager instance."""
    global _locale_manager
    if _locale_manager is None:
        _locale_manager = LocaleManager()
    return _locale_manager


def t(key_path: str, **kwargs) -> str:
    """
    Translate a key path (shorthand for get_locale_manager().get()).

    Args:
        key_path: Dot-separated path like 'cli.init.project_ready'
        **kwargs: Format arguments

    Returns:
        Localized string
    """
    return get_locale_manager().get(key_path, **kwargs)
