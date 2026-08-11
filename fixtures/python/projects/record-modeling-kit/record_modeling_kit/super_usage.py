"""super() usage (PY-CAN-OBJ-004)."""

from __future__ import annotations


class SuperDiamondBase:
    def greet(self) -> str:
        return "base"

    @classmethod
    def kind(cls) -> str:
        return f"base:{cls.__name__}"


class SuperDiamondLeft(SuperDiamondBase):
    def greet(self) -> str:
        return f"left->{super().greet()}"

    @classmethod
    def kind(cls) -> str:
        return f"left->{super().kind()}"


class SuperDiamondRight(SuperDiamondBase):
    def greet(self) -> str:
        return f"right->{super().greet()}"

    @classmethod
    def kind(cls) -> str:
        return f"right->{super().kind()}"


class SuperDiamondLeaf(SuperDiamondLeft, SuperDiamondRight):
    def greet(self) -> str:
        # Zero-argument super() captures __class__ cell.
        return f"leaf->{super().greet()}"

    @classmethod
    def kind(cls) -> str:
        return f"leaf->{super().kind()}"

    def explicit_greet(self) -> str:
        # Explicit form via type and instance.
        return f"explicit->{super(SuperDiamondLeaf, self).greet()}"  # noqa: UP008

    @classmethod
    def explicit_kind(cls) -> str:
        return f"explicit->{super(SuperDiamondLeaf, cls).kind()}"


def zero_arg_demo() -> tuple[str, str]:
    leaf = SuperDiamondLeaf()
    return leaf.greet(), SuperDiamondLeaf.kind()


def explicit_form_demo() -> tuple[str, str]:
    leaf = SuperDiamondLeaf()
    return leaf.explicit_greet(), SuperDiamondLeaf.explicit_kind()


def class_cell_demo() -> bool:
    # __class__ closure cell is implicitly provided for zero-arg super().
    leaf = SuperDiamondLeaf()
    return "__class__" in leaf.greet.__code__.co_freevars or "__class__" in SuperDiamondLeaf.greet.__code__.co_freevars  # type: ignore[attr-defined]


def nested_context_failure_demo() -> str:
    class Outer:
        def method(self) -> str:
            def inner() -> str:
                try:
                    return super().greet()  # type: ignore[misc]
                except RuntimeError as exc:
                    return f"nested-super-failure:{exc}"

            return inner()

        def greet(self) -> str:
            return "outer"

    return Outer().method()


def hardcoded_base_counterexample() -> str:
    class Hardcoded(SuperDiamondLeft):
        def greet(self) -> str:
            # Direct base call bypasses MRO cooperation; contrast with super().
            return f"hardcoded->{SuperDiamondBase.greet(self)}"

    return Hardcoded().greet()
