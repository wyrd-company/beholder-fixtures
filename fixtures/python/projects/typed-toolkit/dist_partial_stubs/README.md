# typed-toolkit-partial-stubs (partial overlay)

Partial stub-only overlay for the `typed-toolkit-partial` runtime distribution.
The `partial_pkg-stubs` package follows the PEP 561 `-stubs` naming and carries a
`py.typed` file containing `partial`, marking it a partial overlay.  Symbols it
omits (e.g. `only_runtime_typed`) fall back to the runtime package's inline types.
