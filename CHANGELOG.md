# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to Spec Mix are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **Note**: This is a fork of [github/spec-kit](https://github.com/github/spec-kit). For the original project's changelog, see the [upstream repository](https://github.com/github/spec-kit/blob/main/CHANGELOG.md).

## [Unreleased]

### Added

- **Multi-Language Support (i18n)**: Full internationalization architecture
  - English and Korean language packs included
  - Locale-specific commands, templates, and CLI messages
  - `spec-mix lang` commands for language management
  - Extensible architecture for community translations
- **Mission System**: Domain-specific workflow templates
  - Software Development mission with feature-based workflows
  - Research mission with academic research workflows
  - Mission-specific commands and templates per language
  - `spec-mix mission` commands for mission management
- **Web Dashboard**: Visual project management interface
  - Feature overview with status tracking
  - Document viewer with markdown rendering
  - Real-time updates and responsive design
  - `spec-mix dashboard` command to launch web server
- **Enhanced Documentation**: Multi-language GitHub Pages
  - Complete English documentation at `/en/`
  - Complete Korean documentation at `/ko/`
  - Language-specific navigation in docs
  - Optimized logos and favicons for GitHub Pages

### Changed

- Repository structure reorganized for i18n support

### Fixed

- Markdown lint issues across locale files
- GitHub Pages logo sizing for navigation bar
- Documentation links updated to new repository

---

## Upstream Spec Kit History

This fork is based on Spec Kit v0.0.20. For the complete history of the upstream project, see:
- [Spec Kit Releases](https://github.com/github/spec-kit/releases)
- [Spec Kit Changelog](https://github.com/github/spec-kit/blob/main/CHANGELOG.md)

