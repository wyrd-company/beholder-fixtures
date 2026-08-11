"""PKG-014 direct-URL provenance modeling."""

from __future__ import annotations

import json
import pathlib

# Model a local direct reference without credentials.
# Installed direct_url.json (PEP 610) example for a local file reference:

DIRECT_URL_DATA = {
    "url": "file:///workspaces/worktrees/beholder/task-427-distributable-suite/fixtures/python/projects/distributable-suite/workspace/suite_workspace_alpha",
    "dir_info": {"editable": False},
}

# For an editable VCS checkout, PEP 610 would add vcs_info with commit etc,
# but we model a local directory reference.

DIRECT_URL_WITH_HASH = {
    "url": "file:///tmp/local_pkg-1.0.tar.gz",
    "archive_info": {"hash": "sha256=abc123"},
}


def write_direct_url(dist_info: pathlib.Path, data: dict = DIRECT_URL_DATA) -> None:
    dist_info.mkdir(parents=True, exist_ok=True)
    (dist_info / "direct_url.json").write_text(json.dumps(data, indent=2), encoding="utf-8")


def read_direct_url(dist_info: pathlib.Path) -> dict:
    return json.loads((dist_info / "direct_url.json").read_text(encoding="utf-8"))


def index_install_has_no_direct_url_note() -> str:
    return "index install (from PyPI) has no direct_url.json; direct reference does"


def no_credentials_note() -> str:
    return "local file reference contains no credentials; URL does not embed user:pass"
