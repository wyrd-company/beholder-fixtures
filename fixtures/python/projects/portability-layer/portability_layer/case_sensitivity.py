"""Case-sensitive import collisions on the local filesystem (PY-CAN-PLAT-002)."""

from __future__ import annotations

import importlib.util
import pathlib
import sys
import tempfile
from dataclasses import dataclass


@dataclass(frozen=True)
class CaseProbe:
    lower_name: str
    upper_name: str
    lower_path: pathlib.Path
    upper_path: pathlib.Path
    case_sensitive: bool


def create_cased_candidates(tmpdir: pathlib.Path) -> CaseProbe:
    """Create two modules differing only in case and report sensitivity.

    On Linux the filesystem is case-sensitive, so ``widget`` and ``Widget``
    are distinct. On case-insensitive volumes they would collide. The result
    records the observed behavior without asserting cross-platform defaults.
    """
    lower = tmpdir / "widget_helper.py"
    upper = tmpdir / "Widget_Helper.py"
    lower.write_text("VALUE = 'lower'\n", encoding="utf-8")
    upper.write_text("VALUE = 'upper'\n", encoding="utf-8")
    sensitive = lower.exists() and upper.exists() and lower.read_text() != upper.read_text()
    # Additional probe: pathlib preserves case even if filesystem folds.
    lexically_distinct = lower.name != upper.name
    _ = lexically_distinct
    return CaseProbe(
        lower_name="widget_helper",
        upper_name="Widget_Helper",
        lower_path=lower,
        upper_path=upper,
        case_sensitive=sensitive,
    )


def import_case_variants(tmpdir: pathlib.Path) -> dict[str, object]:
    """Import differently cased candidates and observe outcomes on this filesystem."""
    probe = create_cased_candidates(tmpdir)
    sys.path.insert(0, str(tmpdir))
    try:
        lower_spec = importlib.util.spec_from_file_location(probe.lower_name, probe.lower_path)
        upper_spec = importlib.util.spec_from_file_location(probe.upper_name, probe.upper_path)
        assert lower_spec is not None and upper_spec is not None
        lower_mod = importlib.util.module_from_spec(lower_spec)
        upper_mod = importlib.util.module_from_spec(upper_spec)
        assert lower_spec.loader is not None and upper_spec.loader is not None
        lower_spec.loader.exec_module(lower_mod)  # type: ignore[attr-defined]
        upper_spec.loader.exec_module(upper_mod)  # type: ignore[attr-defined]
        same_value = lower_mod.VALUE == upper_mod.VALUE  # type: ignore[attr-defined]
        distinct_modules = lower_mod is not upper_mod
        return {
            "probe": probe,
            "lower_value": lower_mod.VALUE,  # type: ignore[attr-defined]
            "upper_value": upper_mod.VALUE,  # type: ignore[attr-defined]
            "same_value": same_value,
            "distinct_modules": distinct_modules,
            "case_sensitive": probe.case_sensitive,
        }
    finally:
        try:
            sys.path.remove(str(tmpdir))
        except ValueError:
            pass


def assert_case_sensitive_filesystem(tmpdir: pathlib.Path) -> bool:
    """Assert that differently cased names are distinct on this Linux filesystem."""
    result = import_case_variants(tmpdir)
    probe: CaseProbe = result["probe"]  # type: ignore[assignment]
    # On the provisioned Linux lane both files must coexist and hold distinct values.
    assert probe.case_sensitive, "expected case-sensitive filesystem on Linux"
    assert result["lower_value"] == "lower"
    assert result["upper_value"] == "upper"
    assert result["distinct_modules"] is True
    return True


def cache_and_vcs_note() -> str:
    """Document cache and version-control nuance for case renames."""
    return (
        "On case-insensitive volumes import caches and version control may treat "
        "a case-only rename as a no-op; on this Linux lane the two spellings are distinct "
        "and importlib resolves each spec independently."
    )


def demonstrate_case_collision_is_filesystem_specific() -> dict[str, object]:
    """Run a temp-dir probe that is valid regardless of volume configuration."""
    with tempfile.TemporaryDirectory() as td:
        tmp = pathlib.Path(td)
        # Create via helper; do not assert universal default, only local observation.
        info = import_case_variants(tmp)
        return {
            "linux_lane_expected_sensitive": True,
            "observed": info["case_sensitive"],
            "note": "Volume configuration overrides OS defaults; assertion limited to local lane.",
        }
