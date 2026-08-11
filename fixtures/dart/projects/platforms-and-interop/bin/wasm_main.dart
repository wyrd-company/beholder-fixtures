/// The WebAssembly entry point, compiled headlessly with
/// `dart compile wasm -o build/wasm_main.wasm bin/wasm_main.dart` to
/// WasmGC — no browser or standalone Wasm/GC-capable runtime is installed,
/// so this project only compiles this target and never runs the output.
/// This is DART-CAN-PLAT-001's `wasm` cell of the compilation-target
/// matrix and DART-CAN-PLAT-005's supported entry point.
///
/// `dart compile wasm` targets the WasmGC proposal exclusively (there is no
/// non-GC Wasm output mode) and requires modern `dart:js_interop`
/// bindings: legacy `dart:html`/`dart:js` do not compile to `wasm` at all,
/// which is DART-CAN-PLAT-005's "modern interop requirement." This entry
/// point shares its interop bindings (`web/js_bindings.dart`,
/// `web/js_conversions.dart`) with `bin/js_main.dart` rather than
/// duplicating them, since both are modern-interop-only and target the
/// same `dart.library.js_interop` conditional branch of
/// `platform/platform_report.dart`.
library;

import 'package:platforms_and_interop/diagnostics/non_portable_observations.dart';
import 'package:platforms_and_interop/platform/platform_report.dart';
import 'package:platforms_and_interop/platform/pragma_catalog.dart';
import 'package:platforms_and_interop/platform/reachability.dart';
import 'package:platforms_and_interop/web/js_bindings.dart';
import 'package:platforms_and_interop/web/js_conversions.dart';

Future<void> main() async {
  print(buildPlatformReport());
  print(describeReachability());
  print('pragmaExamples=${combinePragmaExamples(2, 3)}');

  print('jsMathMax=${jsMathMax(5, 9)}');
  final point = JsPoint(x: 3, y: 4);
  print(
    'point=${point.horizontal},${point.y} jsToString=${point.jsToString()}',
  );

  print('roundTripString=${roundTripString('platforms-and-interop')}');
  final resolved = await resolveJsPromise(13);
  print('resolvedPromise=$resolved');

  print(
    'runtimeTypeObservation='
    '${NonPortableObservations.runtimeTypeObservation(point)}',
  );

  print('wasm platforms-and-interop checks compiled');
}
