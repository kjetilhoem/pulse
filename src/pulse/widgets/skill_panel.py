"""Skill library panel — shows full skill hierarchy."""

from __future__ import annotations

from pathlib import Path

from textual.widgets import Static


class SkillPanel(Static):
    """Shows the complete skill library tree."""

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
        """Scan skill directories and update display with full hierarchy."""
        lines = ["[bold #E94560] SKILL LIBRARY[/]\n"]

        # Universal skills — listed individually
        common_skills = self._list_skills(self.SKILLS_COMMON)
        lines.append(f"  [bold #00FF88]COMMON[/] [#666677]({len(common_skills)})[/]")
        for skill in common_skills:
            lines.append(f"    [#AAAACC]{skill}[/]")

        # Domain packs — each with full skill list
        if self.SKILLS_DOMAINS.exists():
            for domain_dir in sorted(self.SKILLS_DOMAINS.iterdir()):
                if domain_dir.is_dir():
                    skills = self._list_skills(domain_dir)
                    icon = self._domain_icon(domain_dir.name)
                    lines.append("")
                    lines.append(
                        f"  {icon} [bold #00D9FF]{domain_dir.name.upper()}[/] [#666677]({len(skills)})[/]"
                    )
                    for skill in skills:
                        lines.append(f"    [#AAAACC]{skill}[/]")

        total = len(common_skills) + sum(
            len(self._list_skills(d))
            for d in self.SKILLS_DOMAINS.iterdir()
            if d.is_dir()
        ) if self.SKILLS_DOMAINS.exists() else len(common_skills)
        lines.append(f"\n  [#666677]─── {total} skills total ───[/]")

        self.update("\n".join(lines))

    @staticmethod
    def _list_skills(path: Path) -> list[str]:
        """Return sorted list of skill names (without .yaml extension)."""
        if not path.exists():
            return []
        return sorted(p.stem for p in path.glob("*.yaml"))

    @staticmethod
    def _domain_icon(name: str) -> str:
        icons = {
            "audio": "[#FFB800]\u266b[/]",
            "mobile": "[#00FF88]\u25a3[/]",
            "art": "[#E94560]\u2b25[/]",
            "ux": "[#00D9FF]\u25c9[/]",
        }
        return icons.get(name, "[#666677]\u2022[/]")
