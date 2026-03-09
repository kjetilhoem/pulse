"""Skill library panel — shows available skills and domain packs."""

from __future__ import annotations

from pathlib import Path

from textual.widgets import Static


class SkillPanel(Static):
    """Shows skill library stats."""

    DEFAULT_CSS = """
    SkillPanel {
        border: solid $accent;
        padding: 1 2;
        margin: 0 0 1 0;
        height: auto;
    }
    """

    SKILLS_COMMON = Path.home() / ".claude" / "skills" / "common"
    SKILLS_DOMAINS = Path.home() / ".claude" / "skills" / "domains"

    def refresh_skills(self) -> None:
        """Scan skill directories and update display."""
        lines = ["[bold #E94560] SKILL LIBRARY[/]\n"]

        # Universal skills
        common_count = self._count_skills(self.SKILLS_COMMON)
        lines.append(f"  [#00FF88]{common_count}[/] [#AAAACC]universal skills[/]")

        # Domain packs
        if self.SKILLS_DOMAINS.exists():
            lines.append("")
            for domain_dir in sorted(self.SKILLS_DOMAINS.iterdir()):
                if domain_dir.is_dir():
                    count = self._count_skills(domain_dir)
                    icon = self._domain_icon(domain_dir.name)
                    lines.append(
                        f"  {icon} [#00D9FF]{domain_dir.name:<8}[/] [#AAAACC]{count} skills[/]"
                    )

        total = common_count + sum(
            self._count_skills(d)
            for d in self.SKILLS_DOMAINS.iterdir()
            if d.is_dir()
        ) if self.SKILLS_DOMAINS.exists() else common_count
        lines.append(f"\n  [#666677]{total} total[/]")

        self.update("\n".join(lines))

    @staticmethod
    def _count_skills(path: Path) -> int:
        if not path.exists():
            return 0
        return len(list(path.glob("*.yaml")))

    @staticmethod
    def _domain_icon(name: str) -> str:
        icons = {
            "audio": "[#FFB800]\u266b[/]",
            "mobile": "[#00FF88]\u25a3[/]",
            "art": "[#E94560]\u2b25[/]",
            "ux": "[#00D9FF]\u25c9[/]",
        }
        return icons.get(name, "[#666677]\u2022[/]")
