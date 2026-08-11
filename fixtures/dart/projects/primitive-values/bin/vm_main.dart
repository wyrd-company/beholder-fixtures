import 'package:primitive_values/primitive_values.dart';

void main() {
  final sections = <String, List<String>>{
    'DART-CAN-VAL-001 (number-literals)': describeNumberLiterals(),
    'DART-CAN-VAL-001 (arithmetic)': describeArithmetic(),
    'DART-CAN-VAL-001 (special-values)': describeSpecialValues(),
    'DART-CAN-VAL-001 (conversions)': describeConversions(),
    'DART-CAN-VAL-001 (target-observations, vm-jit)':
        describeNumberTargetObservations(),
    'DART-CAN-VAL-002 (string-literals)': describeStringLiterals(),
    'DART-CAN-VAL-002 (interpolation)': describeInterpolation(),
    'DART-CAN-VAL-002 (unicode)': describeUnicode(),
    'DART-CAN-VAL-004 (buffers-and-views)': describeBuffersAndViews(),
    'DART-CAN-VAL-004 (byte-data-endian)': describeByteDataEndian(),
    'DART-CAN-VAL-004 (bounds-and-backing)': describeBoundsAndBacking(),
    'DART-CAN-VAL-004 (backing-observations, vm-jit)':
        describeTypedDataBackingObservations(),
  };

  print('primitive-values vm-jit');
  for (final entry in sections.entries) {
    print('== ${entry.key} ==');
    for (final line in entry.value) {
      print('  $line');
    }
  }
}
