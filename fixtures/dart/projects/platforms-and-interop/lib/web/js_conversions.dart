/// Value, callback, and promise conversions across the JavaScript
/// boundary, matching DART-CAN-PLAT-006. `dart:js_interop` is
/// `js`/`wasm`-only; see `js_bindings.dart` for this project's isolation
/// note.
library;

import 'dart:js_interop';

/// Converts a Dart string to its JS representation and back, demonstrating
/// the `toJS`/`toDart` conversion pair for primitive interop values.
String roundTripString(String value) => value.toJS.toDart;

/// Converts a Dart callback into a JS function value so it can be handed to
/// a JS API that expects a callback (for example `setTimeout` or
/// `addEventListener`).
JSFunction dartCallbackToJs(void Function() callback) => callback.toJS;

@JS('Promise.resolve')
external JSPromise<JSNumber> _resolvedPromise(JSNumber value);

/// Converts a JS `Promise` into a Dart [Future], awaiting the resolved
/// numeric value and converting it back to a Dart [double] —
/// PLAT-006's promise-to-future conversion.
Future<double> resolveJsPromise(double value) async {
  final promise = _resolvedPromise(value.toJS);
  final jsNumber = await promise.toDart;
  return jsNumber.toDartDouble;
}
