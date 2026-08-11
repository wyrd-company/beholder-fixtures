# distributable-suite-native

Full-ABI native extension distribution for PY-CAN-PKG-010 wheel tags.

- Pure wheel tag for other distributions: `py3-none-any`
- Native CPython tag: `cp314-cp314-linux_x86_64` (built on this platform from
  `_native_impl.c`)
- Platform tags: `manylinux_2_34_x86_64` would apply for manylinux builds

The stable-ABI (`abi3`) representative is a separate distribution,
`distributable-suite-native-abi3`, so each wheel carries a single, real,
inspectable compatibility tag.
