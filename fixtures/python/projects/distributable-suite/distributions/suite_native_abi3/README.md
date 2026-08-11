# distributable-suite-native-abi3

Stable-ABI native extension representative for PY-CAN-PKG-010.

The extension is compiled against `Py_LIMITED_API 0x030A0000` (CPython 3.10
limited API) and the distribution sets `bdist_wheel.py-limited-api = cp310`, so
the built wheel carries the `cp310-abi3-<platform>` wheel tag and loads on any
CPython >= 3.10. Contrast with `distributable-suite-native`, whose full-ABI
extension produces a version-specific `cp314-cp314-<platform>` wheel tag.
