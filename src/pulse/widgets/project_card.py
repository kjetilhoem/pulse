"""Project card widget — shows one project's status."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from pulse.data.git_collector import ProjectSnapshot


class ProjectCard(Static):
    """A card showing a single project's status."""

    DEFAULT_CSS = """
    ProjectCard {
        border: solid $accent;
        padding: 1 2;
        margin: 0 1 1 0;
        min-width: 40;
        height: auto;
    }
    ProjectCard .card-title {
        text-style: bold;
        color: #E94560;
    }
    ProjectCard .card-branch {
        color: #00D9FF;
    }
    ProjectCard .card-stats {
        color: #888899;
    }
    ProjectCard .card-commit {
        color: #AAAACC;
    }
    ProjectCard .card-changes {
        color: #FFB800;
    }
    ProjectCard .card-error {
        color: #FF4444;
    }
    """

    def __init__(self, snapshot: ProjectSnapshot) -> None:
        super().__init__()
        self.snapshot = snapshot

    def compose(self) -> ComposeResult:
        s = self.snapshot
        yield Static(f" {s.name.upper()}", classes="card-title")

        if s.error:
            yield Static(f"  {s.error}", classes="card-error")
            return

        yield Static(f"  {s.current_branch}", classes="card-branch")

        stats = f"  {s.total_commits} commits  {len(s.branches)} branches"
        yield Static(stats, classes="card-stats")

        if s.uncommitted_changes > 0:
            yield Static(
                f"  {s.uncommitted_changes} uncommitted changes",
                classes="card-changes",
            )

        # Last 5 commits
        if s.recent_commits:
            yield Static("")
            for c in s.recent_commits[:5]:
                age = _relative_time(c.timestamp)
                yield Static(
                    f"  {c.hash} {c.subject[:40]:<40} {age}",
                    classes="card-commit",
                )


def _relative_time(ts) -> str:
    """Format a datetime as relative time."""
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc)
    if ts.tzinfo is None:
        from datetime import timezone as tz
        ts = ts.replace(tzinfo=tz.utc)
    delta = now - ts
    seconds = int(delta.total_seconds())

    if seconds < 60:
        return "just now"
    if seconds < 3600:
        m = seconds // 60
        return f"{m}m ago"
    if seconds < 86400:
        h = seconds // 3600
        return f"{h}h ago"
    d = seconds // 86400
    return f"{d}d ago"
