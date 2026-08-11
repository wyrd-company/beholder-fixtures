import 'package:primitive_values/primitive_values.dart';

/// Declared entry point for the `js` context: per-target numeric and
/// typed-data observations ([DART-CAN-VAL-001], [DART-CAN-VAL-004]) under
/// headless JavaScript compilation.
void main() {
  print('primitive-values js');
  print('== DART-CAN-VAL-001 (target-observations, js) ==');
  for (final line in describeNumberTargetObservations()) {
    print('  $line');
  }
  print('== DART-CAN-VAL-004 (backing-observations, js) ==');
  for (final line in describeTypedDataBackingObservations()) {
    print('  $line');
  }
}
