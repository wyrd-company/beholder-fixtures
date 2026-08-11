"""Partial stub-only overlay for ``partial_pkg``.

Per PEP 561 the stub package name is the runtime package name with ``-stubs``
appended, and the ``py.typed`` marker contains ``partial`` on its own line.  The
overlay stubs only some symbols; ``only_runtime_typed`` is deliberately omitted
so a checker falls back to the matching runtime distribution's inline types.
"""

partial_value: int

def partial_func(x: int) -> str: ...
