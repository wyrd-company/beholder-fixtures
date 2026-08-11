/// Facade selecting between `platform_report_native.dart` and
/// `platform_report_web.dart` via a `dart.library.js_interop` conditional
/// import/export — the mechanism DART-CAN-PLAT-002 requires for isolating
/// native-only and web-only platform-library imports behind conditional
/// libraries. Every compiled entry point (`bin/vm_main.dart`,
/// `bin/native_aot_main.dart`, `bin/js_main.dart`, `bin/wasm_main.dart`)
/// calls [buildPlatformReport] through this one import, so
/// DART-CAN-PLAT-001's compilation-target matrix and DART-CAN-PLAT-003's
/// same-behavior-in-JIT-and-AOT requirement share a single call site.
library;

export 'platform_report_native.dart'
    if (dart.library.js_interop) 'platform_report_web.dart';

import 'platform_report_native.dart'
    if (dart.library.js_interop) 'platform_report_web.dart'
    as impl;

/// Builds this target's platform report, selected at compile time by the
/// conditional import above.
impl.PlatformReport buildPlatformReport() => impl.buildPlatformReport();
