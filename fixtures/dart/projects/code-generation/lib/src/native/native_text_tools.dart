import 'dart:ffi' as ffi;
import 'dart:io';

import 'package:ffi/ffi.dart' as pkg_ffi;

import 'libc_bindings.g.dart';

/// Handwritten consumer of the ffigen-generated [LibcSubsetBindings]
/// (DART-CAN-BUILD-005): resolves the two symbols the header in
/// `lib/src/native/libc_subset.h` describes. `strnlen` lives in libc;
/// `round` lives in the separate math library, so lookups fall back from
/// one shared object to the other rather than assuming a single library.
class NativeTextTools {
  NativeTextTools()
    : _bindings = LibcSubsetBindings.fromLookup(_lookupAcrossLibcAndLibm);

  final LibcSubsetBindings _bindings;

  static final ffi.DynamicLibrary _libc = ffi.DynamicLibrary.open('libc.so.6');
  static final ffi.DynamicLibrary _libm = ffi.DynamicLibrary.open('libm.so.6');

  static ffi.Pointer<T> _lookupAcrossLibcAndLibm<T extends ffi.NativeType>(
    String symbolName,
  ) {
    try {
      return _libc.lookup<T>(symbolName);
    } on ArgumentError {
      return _libm.lookup<T>(symbolName);
    }
  }

  /// Length of [text] as measured by the generated `strnlen` binding.
  int measuredLength(String text, {int maxLength = 256}) {
    final native = text.toNativeUtf8();
    try {
      return _bindings.strnlen(native.cast(), maxLength);
    } finally {
      pkg_ffi.calloc.free(native);
    }
  }

  /// Nearest integer to [value], via the generated `round` binding.
  double roundToNearest(double value) => _bindings.round(value);
}

/// Documents that this fixture requires no historical Dart toolchain and no
/// preview macro system for code generation (DART-CAN-BUILD-006): every
/// generated artifact in this project — `tool_record.g.dart`,
/// `crate_manifest.crate.g.dart`, `bench_catalog.catalog.g.dart`, and
/// `libc_bindings.g.dart` — is produced by `build_runner`/`source_gen`
/// builders or by `ffigen`, Dart's stable, non-macro generation mechanism.
/// The pinned SDK's experiment set (see the corpus plan overview) is empty
/// by default; no experiment is enabled anywhere in this project, and
/// `Platform.executable` below is read only to document that `dart run`
/// requires no `--enable-experiment` flag for any task in this project.
String describeStableGeneration() =>
    'generated via build_runner/source_gen and ffigen through ${Platform.executable}, no macros';
