import 'dart:io';

import 'package:construction_and_constants/construction_and_constants.dart';

void main() {
  final sections = <String, List<String>>{
    'DART-CAN-OBJ-001 (point)': <String>[
      Point(1, 2).toString(),
      Point.origin().toString(),
    ],
    'DART-CAN-OBJ-001 (anchored-point order)': describeAnchoredPoints(),
    'DART-CAN-OBJ-002 (registry)': describeRegistry(),
    'DART-CAN-OBJ-003 (shape-factory)': describeShapeFactories(),
    'DART-CAN-OBJ-004 (constructor-tearoffs)': describeConstructorTearoffs(),
    'DART-CAN-OBJ-005 (cascades)': describeCascades(),
    'DART-CAN-OBJ-006 (operator-lowering)': describeOperatorLowering(),
    'DART-CAN-CONST-001 (basics)': describeConstantSubset(),
    'DART-CAN-CONST-002 (canonicalization, vm-jit)': describeCanonicalization(),
    'DART-CAN-CONST-003 (equality, vm-jit)': describeEqualityIdentityHashing(),
  };

  stdout.writeln('construction-and-constants vm-jit');
  for (final entry in sections.entries) {
    stdout.writeln('== ${entry.key} ==');
    for (final line in entry.value) {
      stdout.writeln('  $line');
    }
  }
}
