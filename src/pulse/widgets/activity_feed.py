"""Activity feed — live stream of commits across all projects."""

from __future__ import annotations

from textual.widgets import Static

from pulse.data.git_collector import Commit, ProjectSnapshot


class ActivityFeed(Static):
    """Merged timeline of recent activity across all projects."""

    DEFAULT_CSS = """
    ActivityFeed {
        border: solid $accent;
        padding: 1 2;
        margin: 0 0 1 0;
        height: auto;
        min-height: 10;
    }
    """

    def update_feed(self, snapshots: list[ProjectSnapshot]) -> None:
        """Rebuild the feed from all project snapshots."""
        all_commits: list[tuple[str, Commit]] = []
        for snap in snapshots:
            for c in snap.recent_commits:
                all_commits.append((snap.name, c))

        # Sort by timestamp, newest first
        all_commits.sort(key=lambda x: x[1].timestamp, reverse=True)

        lines = ["[bold #E94560] ACTIVITY FEED[/]\n"]
        for project_name, commit in all_commits[:15]:
            tag = f"[#00D9FF]{project_name:<12}[/]"
            hash_str = f"[#666677]{commit.hash}[/]"
            subject = commit.subject[:50]
            lines.append(f"  {tag} {hash_str} {subject}")

        if not all_commits:
            lines.append("  [#666677]No activity yet[/]")

        self.update("\n".join(lines))
