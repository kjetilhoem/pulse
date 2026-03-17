"""Configuration — which projects to monitor."""

from __future__ import annotations

from pathlib import Path

# GitHub owner
GITHUB_OWNER = "kjetilhoem"

# Projects to monitor. Add new entries here.
PROJECTS: list[Path] = [
    Path.home() / "workspace" / "beatsense",
    Path.home() / "workspace" / "pulse",
]

# Refresh interval in seconds
REFRESH_INTERVAL = 30

# Accent colors (shared design language)
CORAL = "#E94560"
CYAN = "#00D9FF"
GREEN = "#00FF88"
AMBER = "#FFB800"
MUTED = "#666677"
