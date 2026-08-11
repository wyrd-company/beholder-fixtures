import 'dart:io';

import 'package:construction_and_constants/construction_and_constants.dart';

/// Declared entry point for the `native-aot` context: canonicalization and
/// identity ([DART-CAN-CONST-002], [DART-CAN-CONST-003]) observed under
/// ahead-of-time compilation, where numeric and NaN identity can differ from
/// `vm-jit`.
void main() {
  stdout.writeln('construction-and-constants native-aot');
  stdout.writeln('== DART-CAN-CONST-002 (canonicalization, native-aot) ==');
  for (final line in describeCanonicalization()) {
    stdout.writeln('  $line');
  }
  stdout.writeln('== DART-CAN-CONST-003 (equality, native-aot) ==');
  for (final line in describeEqualityIdentityHashing()) {
    stdout.writeln('  $line');
  }
}
