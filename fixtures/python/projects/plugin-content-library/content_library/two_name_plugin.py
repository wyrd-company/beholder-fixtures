"""Two-name double execution helper for PY-CAN-MOD-012."""

from content_library.registry import register_content

REGISTRATION_KEY = f"two-name-{__name__}"
register_content(REGISTRATION_KEY, {"source": __name__})
