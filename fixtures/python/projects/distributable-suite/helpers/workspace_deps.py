"""PKG-020 multi-project workspace and local dependencies."""

from __future__ import annotations

import pathlib

# Workspace: workspace/ contains suite_workspace_alpha and suite_workspace_beta
# Beta depends on alpha via `suite-workspace-alpha>=0.2.0` resolved offline from local build.
# Development: sibling import without install works when workspace root is on sys.path:
#   sys.path.insert(0, "workspace/suite_workspace_alpha")
#   import suite_workspace_alpha

# Published: pip install offline from locally built wheels via --find-links dist/


def development_vs_published() -> dict[str, str]:
    return {
        "development": "alpha importable via sys.path without install",
        "editable_combination": "pip install -e workspace/suite_workspace_alpha -e workspace/suite_workspace_beta",
        "published": "pip wheel workspace/suite_workspace_alpha workspace/suite_workspace_beta; pip install --no-index --find-links dist suite-workspace-beta",
        "legacy_requirements": "requirements.txt would list -e ./workspace/suite_workspace_alpha (legacy)",
        "tool_rules": "uv workspace member rules differ from pip find-links",
    }
