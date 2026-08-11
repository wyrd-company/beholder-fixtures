"""Extension stub (PY-CAN-TYPE-016: extension-stub).

Represents the stub for a compiled extension module (``.so`` / ``.pyd``) where
the runtime artifact is not pure Python but a typed stub describes its
interface.
"""

def accelerated_sum(values: list[int]) -> int: ...

class NativeBatch:
    label: str
    def __init__(self, label: str) -> None: ...
    def total(self) -> int: ...
