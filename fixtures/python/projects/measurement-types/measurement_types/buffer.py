"""Buffer protocol and zero-copy views (PY-CAN-PROT-013)."""

from __future__ import annotations

import array


class ByteQuantity:
    """Python-level buffer exporter via ``__buffer__`` (PEP 688, 3.12+)."""

    def __init__(self, data: bytes | bytearray) -> None:
        self._data = bytearray(data)

    def __buffer__(self, flags: int) -> memoryview:
        # ``flags`` is required by the buffer protocol; return view over internal storage
        _ = flags
        return memoryview(self._data)

    def __release_buffer__(self, view: memoryview) -> None:
        # Release hook is optional; acknowledge the view being released
        _ = view

    def as_bytes(self) -> bytes:
        return bytes(self._data)

    def __repr__(self) -> str:
        return f"ByteQuantity({self._data!r})"


def shared_mutation_via_memoryview() -> tuple[int, int]:
    """Mutate exporter through a ``memoryview`` slice."""

    exporter = ByteQuantity(bytearray(b"\x01\x02\x03\x04"))
    view = memoryview(exporter)
    view[1] = 0xFF
    # Mutation is shared: exporter sees the change
    return exporter._data[1], view[1]


def sliced_and_cast_views() -> tuple[bytes, list[int]]:
    """Create sliced and cast ``memoryview`` variants."""

    exporter = ByteQuantity(bytearray(b"\x01\x02\x03\x04\x05\x06\x07\x08"))
    view = memoryview(exporter)
    sliced = view[1:5]
    # Cast bytes view to unsigned short (2 bytes per item) on little-endian
    casted = view.cast("H")
    casted_slice = casted[1:3]
    return bytes(sliced), list(casted_slice)


def release_demo() -> bool:
    """Release a ``memoryview`` explicitly."""

    exporter = ByteQuantity(bytearray(b"\xAA\xBB\xCC"))
    view = memoryview(exporter)
    view.release()
    try:
        _ = view[0]
        return False
    except ValueError:
        return True


def contiguity_and_cast_errors() -> tuple[str, str]:
    """Trigger contiguity and format cast errors."""

    exporter = ByteQuantity(bytearray(b"\x01\x02\x03"))
    view = memoryview(exporter)
    # Cast that violates byte-size alignment
    try:
        view.cast("I", shape=[2])  # type: ignore[arg-type]
        cast_error = "no-error"
    except (TypeError, ValueError):
        cast_error = "cast-error"
    # Contiguity already satisfied for 1-D; force a non-contiguous view via slicing
    sliced = view[::2]
    try:
        sliced.cast("I")
        # Result depends on length alignment; accept either path as valid
        contig_result = "cast-ok"
    except (TypeError, ValueError):
        contig_result = "contiguity-error"
    try:
        sliced.release()
    except ValueError:
        pass
    try:
        view.release()
    except ValueError:
        pass
    return cast_error, contig_result


def exporter_resize_while_viewed() -> str:
    """Resizing the exporter while a view is active raises ``BufferError``."""

    exporter = ByteQuantity(bytearray(b"\x01\x02\x03"))
    view = memoryview(exporter)
    try:
        exporter._data.append(0xFF)
        # Some implementations defer the error until view use or resize check
        _ = view[0]
        # Try explicit resize check
        try:
            view.release()
        except ValueError:
            pass
        return "no-error"
    except BufferError:
        return "buffer-error"
    except ValueError:
        # bytearray resize while exported may raise ValueError on some versions
        return "buffer-error"
    finally:
        try:
            view.release()
        except ValueError:
            pass


def native_exporter_lifetime_demo() -> tuple[bytes, bool]:
    """Native exporter (``bytearray``/``array``) and view lifetime."""

    native = bytearray(b"\x10\x20\x30")
    view = memoryview(native)
    view[0] = 0xFF
    mutated = bytes(native)

    # View keeps exporter alive even after name deletion
    view2 = memoryview(bytearray(b"\x01\x02"))
    exporter_ref = view2.obj  # type: ignore[attr-defined]
    del exporter_ref  # keep view alive
    try:
        _ = view2[0]
        alive = True
    except ValueError:
        alive = False
    try:
        view.release()
    except ValueError:
        pass
    try:
        view2.release()
    except ValueError:
        pass
    return mutated, alive


def array_native_demo() -> tuple[str, list[int]]:
    """Use ``array.array`` as a native buffer exporter."""

    arr = array.array("i", [1, 2, 3, 4])
    view = memoryview(arr)
    casted = view.cast("b")
    # Mutation through cast view propagates to array
    casted[0] = 0x7F
    result = list(arr)
    try:
        casted.release()
    except ValueError:
        pass
    try:
        view.release()
    except ValueError:
        pass
    return arr.typecode, result
