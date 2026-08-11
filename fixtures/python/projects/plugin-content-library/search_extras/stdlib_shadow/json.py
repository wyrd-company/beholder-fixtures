"""Local json that shadows stdlib when earlier on sys.path (PY-CAN-MOD-016)."""

VALUE = "shadow-json"
def shadow_func() -> str:
    return VALUE
