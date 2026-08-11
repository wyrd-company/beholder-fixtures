import 'dart:io';

import 'package:type_model/generics/override_checking.dart';
import 'package:type_model/generics/variance.dart';
import 'package:type_model/runtime_types/runtime_type_tests.dart';

/// Declared entry point for the `native-aot` context: runtime type tests,
/// casts, reified generics ([DART-CAN-TYPE-010]), a variance-inserted
/// runtime write check ([DART-CAN-GEN-003]), and `covariant` parameter and
/// setter runtime checks ([DART-CAN-GEN-004]) observed under ahead-of-time
/// compilation.
void main() {
  stdout.writeln('type-model native-aot');
  stdout.writeln('== DART-CAN-TYPE-010 (runtime type tests, native-aot) ==');
  stdout.writeln('  ${describeRuntimeTypes()}');
  stdout.writeln('== DART-CAN-GEN-003 (variance, native-aot) ==');
  stdout.writeln('  ${describeVariance()}');
  stdout.writeln('== DART-CAN-GEN-004 (override checking, native-aot) ==');
  stdout.writeln('  ${describeOverrideChecking()}');
}
