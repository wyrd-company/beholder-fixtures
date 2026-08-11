# Offline candidate set for PKG-019

- `satisfiable/requests-2.31.0-py3-none-any.whl` (satisfies >=2.28.1)
- `conflict/requests-2.25.0-py3-none-any.whl` (conflicts with suite-core >=2.28.1)

Resolve offline via `uv pip compile --offline --find-links candidate_set --find-links wheelhouse`.

One branch succeeds, one reports true conflict.

This models local candidate set without downloads.
