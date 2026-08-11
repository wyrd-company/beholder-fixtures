# distributable-suite-src

Src-layout distribution (`src/` root) providing the second portion of
`suite_shared_ns` namespace package and a standalone `suite_src` package.

Demonstrates `tool.setuptools.package-dir` and `where = ["src"]` include/exclude
rules, implicit namespace flag (`namespaces = true`), and checkout/install divergence.

Accidental discovery excluded via `exclude = ["tests*"]` (not present).
