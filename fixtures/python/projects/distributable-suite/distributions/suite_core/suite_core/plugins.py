"""Entry-point plugin targets for PY-CAN-DYN-005."""

from __future__ import annotations


def plugin_alpha() -> str:
    return "alpha-plugin-result"


def plugin_beta() -> str:
    return "beta-plugin-result"


PLUGINS = {
    "alpha": plugin_alpha,
    "beta": plugin_beta,
}
