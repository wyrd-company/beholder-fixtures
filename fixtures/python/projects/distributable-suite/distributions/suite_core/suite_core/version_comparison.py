"""PKG-008 version ordering and specifiers demonstration."""

from __future__ import annotations

# Valid version specifiers exercised via dependencies in pyproject.toml:
# compatible release: ~=3.4 (means >=3.4, ==3.*)
# exclusion: !=3.2
# bounded: >=2.0,<4.0
# epoch: 1!2.0.0
# pre: 2.0a1, 2.0b1, 2.0rc1
# post: 2.0.post1
# dev: 2.0.dev0
# local: 2.0+local.1, 2.0+abc.5
# arbitrary equality: ===2.0 (not used, but noted)

VERSION_VARIANTS = [
    "1.0.0",
    "1!2.0.0",  # epoch
    "2.0a1",  # alpha pre-release
    "2.0b1",  # beta
    "2.0rc1",  # release candidate
    "2.0.dev0",  # dev
    "2.0",  # final
    "2.0.post1",  # post
    "2.0+local.1",  # local
    "3.4.1",  # for ~=3.4 compatible
]

# Normalization examples: `requests` vs `Requests` vs `requests` etc handled by packaging.

def is_prerelease(v: str) -> bool:
    return any(tag in v for tag in ("a", "b", "rc", "dev"))


def specifier_examples() -> list[str]:
    return [
        "requests~=3.4",
        "idna!=3.2",
        "charset-normalizer>=2.0,<4.0",
        "legacy-pkg==1!2.0.0",
        "legacy-pkg-pre==2.0a1",
        "legacy-pkg-post==2.0.post1",
        "legacy-pkg-dev==2.0.dev0",
        "legacy-pkg-local==2.0+local.1",
    ]
