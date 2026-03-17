"""Collect open pull requests from GitHub via the gh CLI."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

from pulse.data.config import GITHUB_OWNER


@dataclass
class PullRequest:
    repo: str
    number: int
    title: str
    author: str
    branch: str
    review_status: str  # e.g. "REVIEW_REQUIRED", "APPROVED", "CHANGES_REQUESTED"
    is_draft: bool
    additions: int
    deletions: int
    url: str

    @property
    def needs_action(self) -> bool:
        """PR needs your action if it's review-required or changes-requested."""
        return self.review_status in ("REVIEW_REQUIRED", "CHANGES_REQUESTED")


def collect_prs(projects: list[Path]) -> list[PullRequest]:
    """Fetch open PRs for all monitored projects."""
    prs: list[PullRequest] = []
    for path in projects:
        repo_name = path.name
        full_repo = f"{GITHUB_OWNER}/{repo_name}"
        try:
            result = subprocess.run(
                [
                    "gh", "pr", "list",
                    "--repo", full_repo,
                    "--state", "open",
                    "--json", "number,title,author,headRefName,reviewDecision,isDraft,additions,deletions,url",
                ],
                capture_output=True,
                text=True,
                timeout=15,
            )
            if result.returncode != 0:
                continue
            data = json.loads(result.stdout)
            for item in data:
                prs.append(PullRequest(
                    repo=repo_name,
                    number=item["number"],
                    title=item["title"],
                    author=item.get("author", {}).get("login", "unknown"),
                    branch=item["headRefName"],
                    review_status=item.get("reviewDecision") or "REVIEW_REQUIRED",
                    is_draft=item.get("isDraft", False),
                    additions=item.get("additions", 0),
                    deletions=item.get("deletions", 0),
                    url=item.get("url", ""),
                ))
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError, json.JSONDecodeError):
            continue
    return prs
