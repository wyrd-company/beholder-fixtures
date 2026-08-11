"""Workspace beta package importing alpha."""

try:
    import suite_workspace_alpha
    ALPHA_VALUE = suite_workspace_alpha.VALUE
except ImportError:
    ALPHA_VALUE = "alpha-missing"

VALUE = "beta-value"

def combined() -> str:
    return f"beta+{ALPHA_VALUE}"

def sibling_import_without_install_note() -> str:
    return "beta can import alpha without install when parent workspace is on sys.path"
