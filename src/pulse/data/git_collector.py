"""Collect data from local git repositories."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class Commit:
    hash: str
    subject: str
    author: str
    timestamp: datetime
    branch: str = ""


@dataclass
class BranchInfo:
    name: str
    is_current: bool
    last_commit: str
    ahead: int = 0
    behind: int = 0


@dataclass
class ProjectSnapshot:
    name: str
    path: Path
    branches: list[BranchInfo] = field(default_factory=list)
    recent_commits: list[Commit] = field(default_factory=list)
    current_branch: str = ""
    uncommitted_changes: int = 0
    total_commits: int = 0
    last_activity: datetime | None = None
    error: str | None = None


def _run_git(repo: Path, *args: str) -> str:
    """Run a git command in a repo, return stdout or empty on error."""
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo,
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return ""


def collect_project(path: Path) -> ProjectSnapshot:
    """Collect a snapshot of a git project's state."""
    name = path.name
    snap = ProjectSnapshot(name=name, path=path)

    if not (path / ".git").exists():
        snap.error = "Not a git repository"
        return snap

    # Current branch
    snap.current_branch = _run_git(path, "branch", "--show-current") or "detached"

    # Uncommitted changes
    status = _run_git(path, "status", "--porcelain")
    snap.uncommitted_changes = len(status.splitlines()) if status else 0

    # Recent commits (last 20)
    log = _run_git(
        path, "log", "--oneline", "--format=%H|%s|%an|%aI", "-20"
    )
    if log:
        for line in log.splitlines():
            parts = line.split("|", 3)
            if len(parts) == 4:
                try:
                    ts = datetime.fromisoformat(parts[3])
                except ValueError:
                    ts = datetime.now()
                snap.recent_commits.append(
                    Commit(
                        hash=parts[0][:8],
                        subject=parts[1],
                        author=parts[2],
                        timestamp=ts,
                    )
                )

    if snap.recent_commits:
        snap.last_activity = snap.recent_commits[0].timestamp

    # Total commit count
    count = _run_git(path, "rev-list", "--count", "HEAD")
    snap.total_commits = int(count) if count.isdigit() else 0

    # Branches
    branch_output = _run_git(path, "branch", "-v", "--no-color")
    if branch_output:
        for line in branch_output.splitlines():
            is_current = line.startswith("*")
            parts = line.lstrip("* ").split(None, 2)
            if len(parts) >= 2:
                snap.branches.append(
                    BranchInfo(
                        name=parts[0],
                        is_current=is_current,
                        last_commit=parts[1],
                    )
                )

    return snap


def collect_all(paths: list[Path]) -> list[ProjectSnapshot]:
    """Collect snapshots for all registered projects."""
    return [collect_project(p) for p in paths if p.exists()]
