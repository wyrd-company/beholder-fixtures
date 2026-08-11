"""Absent ``__all__`` — underscore fallback (PY-CAN-MOD-008)."""

public_one = "one"
public_two = "two"
_hidden = "hidden-via-underscore"
ANOTHER = "another"

# No __all__: star import falls back to names not starting with "_".
