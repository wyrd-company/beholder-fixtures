"""Path syntax and object identity (PY-CAN-PLAT-003)."""

from __future__ import annotations

import os
import pathlib
import tempfile
from dataclasses import dataclass


@dataclass(frozen=True)
class PathComparison:
    lexical_equal: bool
    absolute_equal: bool
    resolved_equal: bool
    same_file: bool | None


def lexical_comparison(a: pathlib.Path, b: pathlib.Path) -> bool:
    """Lexical comparison without resolving symlinks or normalizing beyond PurePath."""
    return a == b


def absolute_comparison(a: pathlib.Path, b: pathlib.Path) -> bool:
    """Compare absolute forms."""
    return a.absolute() == b.absolute()


def resolved_comparison(a: pathlib.Path, b: pathlib.Path) -> bool:
    """Compare resolved (symlink-following) forms."""
    return a.resolve() == b.resolve()


def same_file_comparison(a: pathlib.Path, b: pathlib.Path) -> bool | None:
    """Compare via os.path.samefile where available; None if not applicable."""
    try:
        return os.path.samefile(str(a), str(b))
    except OSError:
        return None


def compare_paths(a: pathlib.Path, b: pathlib.Path) -> PathComparison:
    return PathComparison(
        lexical_equal=lexical_comparison(a, b),
        absolute_equal=absolute_comparison(a, b),
        resolved_equal=resolved_comparison(a, b),
        same_file=same_file_comparison(a, b),
    )


class PathIdentity:
    """Helper for lexical, absolute, resolved and same-file comparisons."""

    def __init__(self, base: pathlib.Path) -> None:
        self.base = base

    def variants_for(self, relative: str) -> dict[str, pathlib.Path]:
        p = self.base / relative
        return {
            "relative": pathlib.Path(relative),
            "joined": p,
            "absolute": p.absolute(),
            "resolved": p.resolve(),
        }

    def guarded_symlink_case(self, target_name: str = "origin.txt", link_name: str = "link.txt") -> dict[str, object]:
        """Create a symlink case guarded for POSIX and privilege constraints.

        Returns metadata whether the symlink was created and how comparisons behave.
        """
        target = self.base / target_name
        link = self.base / link_name
        target.write_text("origin", encoding="utf-8")
        supported = False
        created = False
        if os.name == "posix":
            try:
                if link.exists() or link.is_symlink():
                    link.unlink()
                os.symlink(str(target), str(link))
                supported = True
                created = link.is_symlink()
            except OSError:
                supported = False
        comparison = None
        same = None
        if created:
            comparison = compare_paths(target, link)
            same = comparison.same_file
        return {
            "supported": supported,
            "created": created,
            "target": target,
            "link": link,
            "lexical_equal": (target == link),
            "resolved_equal": (target.resolve() == link.resolve()) if created else None,
            "same_file": same,
            "comparison": comparison,
        }

    def guarded_hardlink_case(self, target_name: str = "hard_origin.txt", link_name: str = "hard_link.txt") -> dict[str, object]:
        """Create a hard-link case guarded for POSIX.

        Mirrors symlink handling with os.link semantics.
        """
        target = self.base / target_name
        link = self.base / link_name
        target.write_text("hard-origin", encoding="utf-8")
        supported = False
        created = False
        if os.name == "posix":
            try:
                if link.exists():
                    link.unlink()
                os.link(str(target), str(link))
                supported = True
                created = link.exists()
            except OSError:
                supported = False
        comparison = None
        same = None
        inode_pair: tuple[int, int] | None = None
        if created:
            comparison = compare_paths(target, link)
            same = comparison.same_file
            try:
                inode_pair = (target.stat().st_ino, link.stat().st_ino)
            except OSError:
                inode_pair = None
        return {
            "supported": supported,
            "created": created,
            "target": target,
            "link": link,
            "same_file": same,
            "inode_pair": inode_pair,
            "comparison": comparison,
        }


def demonstrate_identity_suite() -> dict[str, object]:
    """Run an in-tempdir suite covering lexical, absolute, resolved and link cases."""
    with tempfile.TemporaryDirectory() as td:
        base = pathlib.Path(td)
        helper = PathIdentity(base)
        # Lexical difference: "a/./b" vs "a/b" — same resolved, different lexical
        p_a = base / "a" / "." / "b"
        p_b = base / "a" / "b"
        (base / "a" / "b").parent.mkdir(parents=True, exist_ok=True)
        (base / "a" / "b" / "file.txt").parent.mkdir(parents=True, exist_ok=True)
        file_a = base / "a" / "b" / "file.txt"
        file_a.write_text("data", encoding="utf-8")
        lexical = lexical_comparison(p_a / "file.txt", p_b / "file.txt")
        resolved = resolved_comparison(p_a / "file.txt", p_b / "file.txt")
        symlink_case = helper.guarded_symlink_case()
        hardlink_case = helper.guarded_hardlink_case()
        return {
            "lexical_equal_a_dot_b": lexical,
            "resolved_equal_a_dot_b": resolved,
            "symlink": symlink_case,
            "hardlink": hardlink_case,
        }
