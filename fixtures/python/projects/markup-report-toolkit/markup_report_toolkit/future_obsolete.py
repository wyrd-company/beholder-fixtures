"""Obsolete accepted future features (PY-CAN-SRC-003).

``print_function`` and ``unicode_literals`` were once required future
imports; they are now default behavior but remain valid and accepted.
"""

from __future__ import print_function, unicode_literals, with_statement

obsolete_print_function_ok = True
obsolete_unicode_literals_ok = True
obsolete_with_statement_ok = True

def obsolete_demo() -> str:
    # With unicode_literals, string literals would be unicode in Python 2;
    # on Python 3 they are already unicode — import is accepted silently.
    return "unicode"
