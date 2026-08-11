"""Never-imported module for PY-CAN-MOD-012.

Its registry entry would exist only if the module were imported.
Because no other fixture imports it, its absence demonstrates the
``never-imported`` variant.
"""

from content_library.registry import register_content

register_content("never-imported", {"source": "never_imported.py"})
VALUE = "should-not-appear-in-registry"
