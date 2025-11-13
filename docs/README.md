# Spec Mix Documentation

This folder contains the documentation source files for Spec Mix, built using [DocFX](https://dotnet.github.io/docfx/).

## Languages

- **English** - [docs/](.) (default)
- **한국어** - [docs/ko/](ko/)

## Build

The documentation is automatically built and published to GitHub Pages when changes are pushed to the `main` branch.

To build locally:

```bash
cd docs
docfx docfx.json --serve
```

Then open <http://localhost:8080>

## Structure

```text
docs/
├── index.md              # English homepage
├── features.md           # Enhanced features
├── i18n.md              # Multi-language guide
├── missions.md          # Mission system
├── dashboard.md         # Dashboard guide
├── installation.md      # Installation guide
├── quickstart.md        # Quick start guide
├── local-development.md # Development guide
├── toc.yml              # English navigation
└── ko/                  # Korean docs
    ├── index.md
    └── toc.yml
```

## Contributing

To add or update documentation:

1. Edit markdown files
2. Update `toc.yml` if adding new pages
3. Test locally with DocFX
4. Submit PR

For translations, create a new language directory under `docs/[lang-code]/`.
