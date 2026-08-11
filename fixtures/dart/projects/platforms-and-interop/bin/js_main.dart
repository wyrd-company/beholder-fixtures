/// The JavaScript entry point, compiled headlessly with
/// `dart compile js -o build/js_main.js bin/js_main.dart` — no browser is
/// installed, so this project only compiles this target and never runs the
/// output. This is DART-CAN-PLAT-001's `js` cell of the compilation-target
/// matrix and DART-CAN-PLAT-004's web entry.
///
/// DART-CAN-PLAT-004 configuration this project documents rather than
/// exercises at runtime (no browser is available to observe the compiled
/// output):
///
/// - **Numeric semantics**: dart2js represents Dart `int` as a JavaScript
///   `number` outside `Int64List`/`BigInt`-backed paths, so integers
///   exceeding 2^53 lose precision — a target-specific numeric behavior
///   that VM JIT and native AOT, with true 64-bit integers, do not share.
/// - **Deferred loading**: `deferred as` imports (this project's sibling
///   `libraries-and-visibility` project owns DART-CAN-LIB-009's deferred
///   import coverage) become separate output chunks fetched with
///   `loadLibrary()`, letting dart2js split its compiled output into
///   code-splitting units.
/// - **Module configuration**: `dart compile js` emits a single non-modular
///   script by default; passing `--dart2js-args=--experimental-output-format=…`-
///   class flags is how a build selects ES module output instead, a
///   dart2js-specific compiler contract rather than a Dart-language one.
/// - **Minification**: `dart compile js -O2` (or higher) both tree-shakes
///   unreachable declarations more aggressively and renames symbols to
///   short synthetic identifiers; the resulting names are exactly the kind
///   of synthetic-name observation DART-CAN-PLAT-011 records without
///   asserting.
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

  print('jsMathMax=${jsMathMax(3, 7)}');
  final point = JsPoint(x: 1, y: 2);
  point.horizontal = 4;
  print(
    'point=${point.horizontal},${point.y} jsToString=${point.jsToString()}',
  );

  print('roundTripString=${roundTripString('platforms-and-interop')}');
  final callback = dartCallbackToJs(() {});
  print('callbackTypeObservation=${callback.runtimeType}');
  final resolved = await resolveJsPromise(21);
  print('resolvedPromise=$resolved');

  print(
    'runtimeTypeObservation='
    '${NonPortableObservations.runtimeTypeObservation(point)}',
  );

  print('js platforms-and-interop checks compiled');
}
