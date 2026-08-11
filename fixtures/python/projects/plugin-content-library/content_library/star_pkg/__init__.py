"""Star package init — demonstrates explicit imports bypass __all__."""

from .explicit_all import _private as imported_private
__all__ = ["imported_private"]
