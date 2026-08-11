"""PKG-015 reproducible and environment-sensitive builds."""

from __future__ import annotations

import pathlib

# Two builds from equivalent normalized inputs produce equivalent artifacts.
# Normalization: sorted file lists, clamped timestamps (SOURCE_DATE_EPOCH),
# deterministic file order via `sort` in archive creation.

NORMALIZED_INPUTS = [
    "distributions/suite_core/suite_core/_generated_version.py",
    "distributions/suite_core/pyproject.toml",
]

COUNTERCASE = "A build with SOURCE_DATE_EPOCH=0 vs unset produces different timestamps in tar/wheel metadata"


def compare_artifacts(artifact_a: pathlib.Path, artifact_b: pathlib.Path) -> bool:
    """Compare ignoring timestamps: compare sorted namelist and file hashes."""
    import tarfile
    import hashlib

    def tar_hashes(p: pathlib.Path):
        with tarfile.open(p) as tf:
            return sorted((m.name, hashlib.sha256(tf.extractfile(m).read()).hexdigest()) for m in tf.getmembers() if m.isfile())

    try:
        return tar_hashes(artifact_a) == tar_hashes(artifact_b)
    except Exception:
        return False


def countercase_documentation() -> str:
    return (
        "Countercase: building sdist with mtime 2020-01-01 vs 2026-01-01 produces different tar headers; "
        "reproducible builds require SOURCE_DATE_EPOCH and sorted order"
    )


def environment_factors() -> list[str]:
    return ["time (SOURCE_DATE_EPOCH)", "locale", "file order", "paths", "compiler", "generated version drift"]
