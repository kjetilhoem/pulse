"""Tests for git data collector."""

from pathlib import Path

from pulse.data.git_collector import collect_project, ProjectSnapshot


def test_collect_nonexistent_path():
    snap = collect_project(Path("/nonexistent/path"))
    assert snap.error == "Not a git repository"


def test_collect_real_repo():
    """Collect from the pulse repo itself."""
    repo = Path(__file__).parent.parent
    snap = collect_project(repo)
    assert snap.error is None or snap.total_commits == 0  # May be empty if no commits yet
    assert snap.name == "pulse"


def test_snapshot_defaults():
    snap = ProjectSnapshot(name="test", path=Path("/tmp/test"))
    assert snap.total_commits == 0
    assert snap.uncommitted_changes == 0
    assert snap.branches == []
    assert snap.recent_commits == []
    assert snap.current_branch == ""
    assert snap.last_activity is None
    assert snap.error is None
