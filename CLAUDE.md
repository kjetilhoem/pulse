# Pulse — Project Management Dashboard

## What This Is
A multi-platform dashboard that visualizes activity across Kjetil's project portfolio. Eye-pleasing, real-time, with a show-off factor.

## Tech Stack
- **macOS TUI**: Python 3 + Textual (rich terminal UI framework)
- **Android**: Kotlin + Jetpack Compose (future)
- **Data**: Git repos as source of truth — commits, branches, PRs, build status

## Build & Run
```bash
# Install dependencies
pip install -e ".[dev]"

# Run the TUI
python -m pulse

# Run tests
pytest
```

## Architecture
- `src/pulse/` — main package
- `src/pulse/data/` — git and GitHub data collection
- `src/pulse/widgets/` — Textual UI components
- `src/pulse/app.py` — main Textual application
- `tests/` — pytest tests

## Design Language
- Dark background, luminous accents
- Primary accent: coral #E94560 (shared with BeatSense)
- Secondary: cyan #00D9FF, green #00FF88, amber #FFB800
- Monospace typography, clean grids
- Animated transitions where possible
- The aesthetic goal: a mission control screen that looks like it belongs in a sci-fi film

## Git Workflow
- **Never push directly to main.** Always create a feature branch and open a PR.
- Branch naming: `feature/<short-description>` or `fix/<short-description>`
- PRs require review before merging — do not auto-merge.

## Conventions
- All paths use absolute references
- Git operations are read-only (never modify repos from the dashboard)
- Data refresh on configurable interval (default 30s)
- Graceful handling of missing repos or network
