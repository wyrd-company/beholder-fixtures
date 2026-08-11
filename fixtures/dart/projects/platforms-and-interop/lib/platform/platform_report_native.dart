/// The native-only half of DART-CAN-PLAT-002's conditional platform-library
/// isolation, selected — alongside `platform_report_web.dart` — by
/// `platform_report.dart`'s `dart.library.js_interop` conditional
/// import/export. Bundles `dart:io`, `dart:ffi`, and `dart:isolate` —
/// three of the five libraries the checklist names as native-only —
/// because all three are available together on both VM JIT and native AOT
/// and unavailable together on `js` and `wasm`.
///
/// `dart:mirrors`, the checklist's fourth native-only library, is JIT-only
/// rather than native-only (native AOT rejects it too), so it cannot share
/// this native/web conditional: no `dart.library.*` condition distinguishes
/// VM JIT from native AOT, since both take this file's branch. It is
/// isolated separately as a dedicated JIT-only source set instead; see
/// `reflect/reflective_registry.dart`.
library;

import 'dart:ffi';
import 'dart:io';
import 'dart:isolate';

/// A capability report assembled from three native-only platform
/// libraries.
final class PlatformReport {
  const PlatformReport({
    required this.operatingSystem,
    required this.pointerSizeBytes,
    required this.isolateDebugName,
  });

  /// From `dart:io`'s [Platform.operatingSystem].
  final String operatingSystem;

  /// From `dart:ffi`'s [sizeOf], the native pointer width for this target.
  final int pointerSizeBytes;

  /// From `dart:isolate`'s [Isolate.current].
  final String isolateDebugName;

  @override
  String toString() =>
      'native(os: $operatingSystem, pointerBytes: $pointerSizeBytes, '
      'isolate: $isolateDebugName)';
}

/// Builds a [PlatformReport] from the three native-only platform libraries
/// this file bundles.
PlatformReport buildPlatformReport() => PlatformReport(
  operatingSystem: Platform.operatingSystem,
  pointerSizeBytes: sizeOf<IntPtr>(),
  isolateDebugName: Isolate.current.debugName ?? 'unnamed',
);
