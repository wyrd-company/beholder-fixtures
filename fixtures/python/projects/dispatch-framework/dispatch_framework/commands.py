"""Command dispatch through stored callables (PY-CAN-DYN-011)."""

from __future__ import annotations

import argparse
from typing import Callable

# Handler name versus key: registry key need not match function __name__.


def handle_create(args: argparse.Namespace) -> str:
    return f"create:{args.label}"


def handle_remove(args: argparse.Namespace) -> str:
    return f"remove:{args.label}"


def handle_list(args: argparse.Namespace) -> str:  # noqa: A001 — name is intentional
    return f"list:{args.detail}"


# Stored callables as data; signature becomes interface (args: Namespace).
COMMAND_TABLE: dict[str, Callable[[argparse.Namespace], str]] = {
    "create": handle_create,
    "delete": handle_remove,  # key differs from function name
    "list": handle_list,
}

# Subcommand table.
SUBCOMMAND_TABLE: dict[str, dict[str, Callable[[argparse.Namespace], str]]] = {
    "catalog": {
        "add": handle_create,
        "rm": handle_remove,
    }
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dispatch")
    sub = parser.add_subparsers(dest="command", required=True)
    p_create = sub.add_parser("create")
    p_create.add_argument("label")
    p_create.set_defaults(handler=COMMAND_TABLE["create"])

    p_delete = sub.add_parser("delete")
    p_delete.add_argument("label")
    p_delete.set_defaults(handler=COMMAND_TABLE["delete"])

    p_list = sub.add_parser("list")
    p_list.add_argument("--detail", default="summary")
    p_list.set_defaults(handler=COMMAND_TABLE["list"])

    # Subcommand nesting: catalog add / catalog rm
    p_catalog = sub.add_parser("catalog")
    cat_sub = p_catalog.add_subparsers(dest="catalog_cmd", required=True)
    c_add = cat_sub.add_parser("add")
    c_add.add_argument("label")
    c_add.set_defaults(handler=SUBCOMMAND_TABLE["catalog"]["add"])
    c_rm = cat_sub.add_parser("rm")
    c_rm.add_argument("label")
    c_rm.set_defaults(handler=SUBCOMMAND_TABLE["catalog"]["rm"])
    return parser


def dispatch_command(argv: list[str]) -> str:
    parser = build_parser()
    try:
        ns = parser.parse_args(argv)
    except SystemExit as exc:
        return f"parse-error:{exc.code}"
    handler: Callable[[argparse.Namespace], str] | None = getattr(ns, "handler", None)
    if handler is None:
        return "missing-handler"
    # Indirect invocation through stored callable.
    if handler not in COMMAND_TABLE.values() and handler not in SUBCOMMAND_TABLE["catalog"].values():
        # Entry-point wiring variant: handler could have come from dotted path, still valid.
        pass
    # Stale/missing handler counterexample: lookup by string key.
    if isinstance(handler, str):  # would be stale if stored as string not callable
        return "stale-handler-string"
    return handler(ns)


def stale_handler_demo() -> str:
    # Simulate stale rename: stored string no longer resolves.
    stale_table: dict[str, str] = {"old_create": "dispatch_framework.commands.handle_create_old"}
    name = stale_table["old_create"]
    return f"stale:{name}"
