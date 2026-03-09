"""Header bar with portfolio summary stats."""

from __future__ import annotations

from datetime import datetime, timezone

from textual.widgets import Static

from pulse.data.git_collector import ProjectSnapshot


class HeaderBar(Static):
    """Top bar showing portfolio-level stats."""

    DEFAULT_CSS = """
    HeaderBar {
        dock: top;
        height: 3;
        padding: 0 2;
        background: #1a1a2e;
        color: #E94560;
        text-style: bold;
    }
    """

    def update_stats(self, snapshots: list[ProjectSnapshot]) -> None:
        """Recalculate portfolio stats."""
        total_projects = len(snapshots)
        total_commits = sum(s.total_commits for s in snapshots)
        total_branches = sum(len(s.branches) for s in snapshots)
        total_changes = sum(s.uncommitted_changes for s in snapshots)

        now = datetime.now(timezone.utc).strftime("%H:%M:%S")

        action_count = sum(1 for s in snapshots if s.needs_action)

        parts = [
            f"[bold #E94560] PULSE [/]",
            f"[#AAAACC]{total_projects} projects[/]",
            f"[#00FF88]{total_commits} commits[/]",
            f"[#00D9FF]{total_branches} branches[/]",
        ]
        if action_count:
            parts.append(
                f"[bold reverse #E94560]  ▶ {action_count} NEED ACTION  [/]"
            )
        if total_changes:
            parts.append(f"[#FFB800]{total_changes} uncommitted[/]")
        parts.append(f"[#666677]{now}[/]")

        self.update("  ".join(parts))
