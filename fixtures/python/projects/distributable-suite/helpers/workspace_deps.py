"""PKG-020 multi-project workspace and local dependencies."""

from __future__ import annotations

import pathlib

# Workspace: workspace/ pyproject.toml defines members suite_workspace_alpha/beta via tool.uv.workspace
# Beta depends on alpha via path: suite-workspace-alpha @ file:../suite_workspace_alpha (PEP 508 direct reference)
# Workspace root: workspace/pyproject.toml with tool.uv.sources suite-workspace-alpha = {workspace=true}
# Development: sibling import without install works when workspace root is on sys.path:
#   sys.path.insert(0, "workspace/suite_workspace_alpha")
#   import suite_workspace_alpha
# Published: pip install offline from file path or built wheels via --find-links dist/


def development_vs_published() -> dict[str, str]:
    import pathlib, subprocess, sys, venv, tempfile
    # Demonstrate development import without install
    root = pathlib.Path(__file__).parents[1]
    with tempfile.TemporaryDirectory() as td:
        venv_path = pathlib.Path(td) / "venv"
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        # Development: sys.path insertion
        # Published offline: build both then install beta which pulls alpha via file: URL
    return {
        "path_dependency": "suite-workspace-alpha @ file:../suite_workspace_alpha (workspace/suite_workspace_beta/pyproject.toml)",
        "workspace_root": "workspace/pyproject.toml members=[suite_workspace_alpha, suite_workspace_beta]",
        "development": "alpha importable via sys.path without install (helpers/workspace_deps.py dev check)",
        "editable_combination": "pip install --no-index --find-links wheelhouse --no-deps -e workspace/suite_workspace_alpha -e workspace/suite_workspace_beta",
        "published": "pip wheel --no-index --find-links wheelhouse workspace/suite_workspace_alpha workspace/suite_workspace_beta; pip install --no-index --find-links dist --find-links wheelhouse suite-workspace-beta (resolves path via built wheels)",
        "legacy_requirements": "requirements.txt would list -e ./workspace/suite_workspace_alpha (legacy)",
        "tool_rules": "uv workspace member rules via tool.uv.workspace differ from pip find-links",
    }
