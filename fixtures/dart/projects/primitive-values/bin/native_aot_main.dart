import 'package:primitive_values/primitive_values.dart';

/// Declared entry point for the `native-aot` context: per-target numeric
/// and typed-data observations ([DART-CAN-VAL-001], [DART-CAN-VAL-004])
/// under native ahead-of-time compilation.
void main() {
  print('primitive-values native-aot');
  print('== DART-CAN-VAL-001 (target-observations, native-aot) ==');
  for (final line in describeNumberTargetObservations()) {
    print('  $line');
  }
  print('== DART-CAN-VAL-004 (backing-observations, native-aot) ==');
  for (final line in describeTypedDataBackingObservations()) {
    print('  $line');
  }
}
