import 'package:primitive_values/primitive_values.dart';

/// Declared entry point for the `wasm` context: per-target numeric and
/// typed-data observations ([DART-CAN-VAL-001], [DART-CAN-VAL-004]) under
/// headless WebAssembly compilation.
void main() {
  print('primitive-values wasm');
  print('== DART-CAN-VAL-001 (target-observations, wasm) ==');
  for (final line in describeNumberTargetObservations()) {
    print('  $line');
  }
  print('== DART-CAN-VAL-004 (backing-observations, wasm) ==');
  for (final line in describeTypedDataBackingObservations()) {
    print('  $line');
  }
}
