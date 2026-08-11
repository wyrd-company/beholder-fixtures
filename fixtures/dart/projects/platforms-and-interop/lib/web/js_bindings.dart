/// Modern JavaScript interop bindings, matching DART-CAN-PLAT-006 and
/// DART-CAN-FN-005. `dart:js_interop` is `js`/`wasm`-only, so this library
/// is reachable only through `platform_report.dart`'s conditional web
/// branch and this project's `js`/`wasm` entry points, never from
/// `bin/vm_main.dart` or `bin/native_aot_main.dart`.
library;

import 'dart:js_interop';

/// An external top-level function bound to the global `Math.max`, FN-005's
/// JavaScript-interop external-function representative.
@JS('Math.max')
external double jsMathMax(double a, double b);

/// A JavaScript point object, modeled as an extension type over
/// [JSObject]. Extension types have no runtime representation of their
/// own: at runtime, a [JsPoint] value is exactly its underlying
/// [JSObject], a fact recorded as a non-portable observation rather than
/// asserted (see `diagnostics/non_portable_observations.dart`).
extension type JsPoint._(JSObject _) implements JSObject {
  /// An external factory constructor, FN-005's external-constructor
  /// representative, mapped to the JavaScript object literal `{x, y}`.
  external factory JsPoint({required double x, required double y});

  /// An external getter, FN-005's external-getter representative. The
  /// Dart member name matches the JS property name implicitly; no
  /// `@JS(...)` rename is needed here.
  external double get y;

  /// An external getter mapped to a differently named JS property (`x`
  /// exposed under the Dart name `horizontal`), demonstrating PLAT-006's
  /// name-mapping requirement.
  @JS('x')
  external double get horizontal;

  /// An external setter, FN-005's external-setter representative, paired
  /// with [horizontal] for the same renamed property.
  @JS('x')
  external set horizontal(double value);

  /// An external method, FN-005's external-method representative, mapped
  /// to the JS instance method `toString`.
  @JS('toString')
  external JSString jsToString();
}
