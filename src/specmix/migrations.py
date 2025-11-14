"""
Project migration system for Spec Mix.

Manages version-to-version migrations when project structure or features change.
Similar to database migrations in Django/Rails.
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional, Callable, Dict, Any
from abc import ABC, abstractmethod
from packaging import version


class Migration(ABC):
    """Base class for migrations."""

    # Version this migration upgrades FROM
    version_from: str = "0.0.0"

    # Version this migration upgrades TO
    version_to: str = "0.0.1"

    # Migration description
    description: str = "Base migration"

    @abstractmethod
    def upgrade(self, project_path: Path) -> bool:
        """
        Perform the upgrade migration.

        Args:
            project_path: Path to the project directory

        Returns:
            True if successful, False otherwise
        """
        pass

    def can_upgrade(self, project_path: Path) -> bool:
        """
        Check if this migration can be applied.

        Args:
            project_path: Path to the project directory

        Returns:
            True if migration can be applied
        """
        return True

    def downgrade(self, project_path: Path) -> bool:
        """
        Optional: Rollback this migration.

        Args:
            project_path: Path to the project directory

        Returns:
            True if successful, False otherwise
        """
        raise NotImplementedError("Downgrade not implemented for this migration")


class SymlinkCommandsMigration(Migration):
    """
    Migration to convert copied command files to symlinks.

    Version: 0.0.1-alpha.1 → 0.0.1-alpha.2

    Changes:
    - Converts .claude/commands/ (and other agent folders) from copied files to symlinks
    - Points to .spec-mix/active-mission/commands/
    """

    version_from = "0.0.1-alpha.1"
    version_to = "0.0.1-alpha.2"
    description = "Convert agent command directories to symlinks"

    # List of agent folders that might have commands
    AGENT_FOLDERS = [
        ".claude",
        ".github",
        ".gemini",
        ".cursor",
        ".qwen",
        ".opencode",
        ".codex",
        ".windsurf",
        ".kilocode",
        ".augment",
        ".codebuddy",
        ".amp",
        ".q"
    ]

    def upgrade(self, project_path: Path) -> bool:
        """Convert copied commands to symlinks."""
        try:
            mission_commands_dir = project_path / ".spec-mix" / "active-mission" / "commands"

            # Check if mission commands exist
            if not mission_commands_dir.exists():
                print(f"Warning: {mission_commands_dir} does not exist. Skipping migration.")
                return True

            migrated_count = 0

            for agent_folder in self.AGENT_FOLDERS:
                agent_commands_dir = project_path / agent_folder / "commands"

                # Skip if agent folder doesn't exist
                if not agent_commands_dir.exists() and not agent_commands_dir.is_symlink():
                    continue

                # Skip if already a symlink
                if agent_commands_dir.is_symlink():
                    print(f"  ✓ {agent_folder}/commands is already a symlink")
                    continue

                # Backup existing directory
                backup_dir = agent_commands_dir.parent / "commands.backup"
                if agent_commands_dir.exists():
                    print(f"  • Backing up {agent_folder}/commands → {agent_folder}/commands.backup")
                    if backup_dir.exists():
                        shutil.rmtree(backup_dir)
                    shutil.move(str(agent_commands_dir), str(backup_dir))

                # Create symlink
                try:
                    rel_target = os.path.relpath(mission_commands_dir, agent_commands_dir.parent)
                    agent_commands_dir.symlink_to(rel_target, target_is_directory=True)
                    print(f"  ✓ Created symlink: {agent_folder}/commands → .spec-mix/active-mission/commands")
                    migrated_count += 1

                except (OSError, NotImplementedError) as e:
                    # Restore backup if symlink failed
                    print(f"  ⚠ Symlink failed for {agent_folder}/commands (Windows?), restoring backup")
                    if backup_dir.exists():
                        shutil.move(str(backup_dir), str(agent_commands_dir))
                    continue

            if migrated_count > 0:
                print(f"\n✓ Migrated {migrated_count} agent command director{'y' if migrated_count == 1 else 'ies'} to symlinks")
            else:
                print("\n✓ No migration needed (already using symlinks or no agents found)")

            return True

        except Exception as e:
            print(f"✗ Migration failed: {e}")
            return False

    def can_upgrade(self, project_path: Path) -> bool:
        """Check if migration can be applied."""
        # Check if .spec-mix/active-mission/commands exists
        mission_commands = project_path / ".spec-mix" / "active-mission" / "commands"
        return mission_commands.exists()


class MigrationRegistry:
    """Registry of all available migrations."""

    def __init__(self):
        self.migrations: List[Migration] = []

    def register(self, migration: Migration):
        """Register a migration."""
        self.migrations.append(migration)

    def get_migration_chain(self, from_version: str, to_version: str) -> List[Migration]:
        """
        Get ordered list of migrations needed to go from one version to another.

        Args:
            from_version: Starting version
            to_version: Target version

        Returns:
            List of migrations in order
        """
        from_ver = version.parse(from_version)
        to_ver = version.parse(to_version)

        # Filter and sort applicable migrations
        applicable = [
            m for m in self.migrations
            if version.parse(m.version_from) >= from_ver
            and version.parse(m.version_to) <= to_ver
        ]

        # Sort by version_from
        applicable.sort(key=lambda m: version.parse(m.version_from))

        return applicable

    def get_all_migrations(self) -> List[Migration]:
        """Get all registered migrations sorted by version."""
        return sorted(self.migrations, key=lambda m: version.parse(m.version_from))


# Global registry
_registry = MigrationRegistry()

# Register all migrations
_registry.register(SymlinkCommandsMigration())


def get_registry() -> MigrationRegistry:
    """Get the global migration registry."""
    return _registry


def get_project_version(project_path: Path) -> Optional[str]:
    """
    Get the current version of a Spec Mix project.

    Args:
        project_path: Path to the project directory

    Returns:
        Version string or None if not found
    """
    version_file = project_path / ".spec-mix" / "version"

    if version_file.exists():
        try:
            with open(version_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception:
            pass

    # Fallback: check config.json
    config_file = project_path / ".spec-mix" / "config.json"
    if config_file.exists():
        try:
            import json
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('spec_mix_version')
        except Exception:
            pass

    # Default to oldest version if not found
    return "0.0.1-alpha.1"


def set_project_version(project_path: Path, new_version: str):
    """
    Set the project version.

    Args:
        project_path: Path to the project directory
        new_version: Version string to set
    """
    spec_mix_dir = project_path / ".spec-mix"
    spec_mix_dir.mkdir(exist_ok=True)

    version_file = spec_mix_dir / "version"
    with open(version_file, 'w', encoding='utf-8') as f:
        f.write(new_version)

    # Also update config.json if it exists
    config_file = spec_mix_dir / "config.json"
    if config_file.exists():
        try:
            import json
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            config['spec_mix_version'] = new_version

            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not update config.json: {e}")


def run_migrations(
    project_path: Path,
    target_version: Optional[str] = None,
    dry_run: bool = False
) -> bool:
    """
    Run migrations to upgrade project to target version.

    Args:
        project_path: Path to the project directory
        target_version: Target version (None = latest)
        dry_run: If True, only show what would be done

    Returns:
        True if successful, False otherwise
    """
    registry = get_registry()
    all_migrations = registry.get_all_migrations()

    if not all_migrations:
        print("ℹ No migrations available in the system")
        return True

    if target_version is None:
        # Get latest version from registry
        target_version = all_migrations[-1].version_to

    current_version = get_project_version(project_path)
    print(f"Current version: {current_version}")
    print(f"Target version:  {target_version}")

    # Check if already at target version
    current_ver = version.parse(current_version)
    target_ver = version.parse(target_version)

    if current_ver >= target_ver:
        print(f"\n✓ Already at version {current_version} (no migration needed)")
        return True

    # Get migration chain
    migrations = registry.get_migration_chain(current_version, target_version)

    if not migrations:
        print(f"\n⚠ No migration path found from {current_version} to {target_version}")
        print("\nAvailable migrations:")
        for mig in all_migrations:
            print(f"  • {mig.version_from} → {mig.version_to}: {mig.description}")
        return False

    print(f"\nFound {len(migrations)} migration(s) to apply:\n")

    for i, migration in enumerate(migrations, 1):
        print(f"{i}. {migration.description}")
        print(f"   {migration.version_from} → {migration.version_to}")

    if dry_run:
        print("\n[DRY RUN] No changes made")
        return True

    print("\nApplying migrations...\n")

    # Run migrations
    for migration in migrations:
        print(f"Running: {migration.description}")

        if not migration.can_upgrade(project_path):
            print(f"  ⚠ Skipping (preconditions not met)")
            continue

        success = migration.upgrade(project_path)

        if not success:
            print(f"\n✗ Migration failed: {migration.description}")
            return False

        # Update version after successful migration
        set_project_version(project_path, migration.version_to)

    print(f"\n✓ Successfully migrated to {target_version}")
    return True
