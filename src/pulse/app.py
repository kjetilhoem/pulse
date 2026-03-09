"""Pulse — the main Textual application."""

from __future__ import annotations

from textual.app import App, ComposeResult
from textual.containers import Horizontal, ScrollableContainer, Vertical
from textual.widgets import Footer, Static

from pulse.data.config import PROJECTS, REFRESH_INTERVAL
from pulse.data.git_collector import collect_all
from pulse.widgets.activity_feed import ActivityFeed
from pulse.widgets.header_bar import HeaderBar
from pulse.widgets.project_card import ProjectCard
from pulse.widgets.skill_panel import SkillPanel


class PulseApp(App):
    """Mission control for your project portfolio."""

    TITLE = "Pulse"
    SUB_TITLE = "Project Dashboard"

    CSS = """
    Screen {
        background: #0f0f23;
    }

    #main-layout {
        height: 1fr;
    }

    #left-panel {
        width: 2fr;
        padding: 1;
    }

    #right-panel {
        width: 1fr;
        padding: 1;
    }

    #project-grid {
        height: auto;
    }

    .section-title {
        text-style: bold;
        color: #E94560;
        padding: 0 0 1 1;
    }

    Footer {
        background: #1a1a2e;
    }
    """

    BINDINGS = [
        ("r", "refresh", "Refresh"),
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield HeaderBar(id="header")

        with Horizontal(id="main-layout"):
            with ScrollableContainer(id="left-panel"):
                yield Static(" PROJECTS", classes="section-title")
                with Vertical(id="project-grid"):
                    pass  # Populated on mount
                yield Static("")
                yield ActivityFeed(id="feed")

            with Vertical(id="right-panel"):
                yield SkillPanel(id="skills")

        yield Footer()

    def on_mount(self) -> None:
        """Initial data load and start refresh timer."""
        self._refresh_data()
        self.set_interval(REFRESH_INTERVAL, self._refresh_data)

    def action_refresh(self) -> None:
        """Manual refresh (R key)."""
        self._refresh_data()

    def _refresh_data(self) -> None:
        """Collect data from all projects and update UI."""
        snapshots = collect_all(PROJECTS)

        # Update header
        header = self.query_one("#header", HeaderBar)
        header.update_stats(snapshots)

        # Update project cards
        grid = self.query_one("#project-grid", Vertical)
        grid.remove_children()
        for snap in snapshots:
            grid.mount(ProjectCard(snap))

        # Update activity feed
        feed = self.query_one("#feed", ActivityFeed)
        feed.update_feed(snapshots)

        # Update skill panel
        skills = self.query_one("#skills", SkillPanel)
        skills.refresh_skills()
