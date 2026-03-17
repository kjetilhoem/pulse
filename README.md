# Pulse

A multi-platform dashboard that visualizes activity across Kjetil's project portfolio. Real-time, eye-pleasing, with a show-off factor.

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

## Project Structure
```
src/pulse/
├── app.py                  # Main Textual application
├── data/
│   ├── config.py           # Configuration
│   └── git_collector.py    # Git data collection
└── widgets/
    ├── activity_feed.py    # Activity feed widget
    ├── header_bar.py       # Header bar widget
    ├── project_card.py     # Project card widget
    └── skill_panel.py      # Skill panel widget
tests/                      # pytest tests
```

## Design Language
- Dark background, luminous accents
- Primary accent: coral #E94560 (shared with BeatSense)
- Secondary: cyan #00D9FF, green #00FF88, amber #FFB800
- The aesthetic goal: a mission control screen that looks like it belongs in a sci-fi film

## License

MIT
