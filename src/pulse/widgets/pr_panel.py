"""Pull request panel — shows open PRs needing attention."""

from __future__ import annotations

from textual.widgets import Static

from pulse.data.github_collector import PullRequest


class PrPanel(Static):
    """Shows open pull requests, highlighting those needing action."""

    DEFAULT_CSS = """
    PrPanel {
        border: solid $accent;
        padding: 1 2;
        margin: 0 0 1 0;
        height: auto;
        min-height: 6;
    }
    """

    def update_prs(self, prs: list[PullRequest]) -> None:
        """Rebuild the PR display."""
        action_prs = [p for p in prs if p.needs_action]
        other_prs = [p for p in prs if not p.needs_action]

        lines = ["[bold #E94560] PULL REQUESTS[/]\n"]

        if action_prs:
            lines.append(
                f"  [bold reverse #E94560]  ▶ {len(action_prs)} NEED YOUR ACTION  [/]\n"
            )
            for pr in action_prs:
                lines.append(_format_pr(pr, highlight=True))
            if other_prs:
                lines.append("")

        for pr in other_prs:
            lines.append(_format_pr(pr, highlight=False))

        if not prs:
            lines.append("  [#666677]No open PRs[/]")

        self.update("\n".join(lines))


def _format_pr(pr: PullRequest, *, highlight: bool) -> str:
    """Format a single PR line."""
    repo_tag = f"[#00D9FF]{pr.repo:<12}[/]"
    number = f"[#666677]#{pr.number:<4}[/]"
    diff = f"[#00FF88]+{pr.additions}[/][#666677]/[/][#E94560]-{pr.deletions}[/]"

    if highlight:
        status = _status_badge(pr.review_status)
        title = f"[bold #FFB800]{pr.title[:38]}[/]"
        draft = " [#666677](draft)[/]" if pr.is_draft else ""
        return f"  ⚡ {repo_tag} {number} {title}{draft}  {diff}  {status}"
    else:
        title = f"[#AAAACC]{pr.title[:38]}[/]"
        draft = " [#666677](draft)[/]" if pr.is_draft else ""
        status_tag = f"[#00FF88]✓ approved[/]"
        return f"     {repo_tag} {number} {title}{draft}  {diff}  {status_tag}"


def _status_badge(status: str) -> str:
    """Return a colored badge for the review status."""
    badges = {
        "REVIEW_REQUIRED": "[bold #FFB800]⏳ review needed[/]",
        "CHANGES_REQUESTED": "[bold #E94560]✗ changes requested[/]",
    }
    return badges.get(status, f"[#666677]{status}[/]")
