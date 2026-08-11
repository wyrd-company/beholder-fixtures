# Vendored wheelhouse

This directory vendors the sole third-party build dependency
`setuptools==84.0.0` for isolated offline builds.

- Wheel: `setuptools-84.0.0-py3-none-any.whl`
  SHA-256 `51a52592b3b99e102b609654876bd65f19f999935166d1352678931132b0c670`
- Source distribution: `setuptools-84.0.0.tar.gz`
  SHA-256 `f4695c21257f0d9b537ec2692c941d02ee143b7cc1276941349a546573b2ef73`
- Source: https://pypi.org/project/setuptools/84.0.0/
- License: MIT (see `LICENSE` and `NOTICE`)

Isolated builds stay enabled; `pip` resolves the backend via
`--no-index --find-links wheelhouse` without downloads.

No `setup_requires` is declared; `get_requires_for_build_*` hooks return
an empty list per upstream `setuptools.build_meta` 84.0.0 lines 265-310
and 435-438.
