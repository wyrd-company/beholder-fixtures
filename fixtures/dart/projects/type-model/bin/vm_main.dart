import 'dart:io';

import 'package:type_model/aliases/type_aliases.dart';
import 'package:type_model/classes/modifiers_boundary.dart';
import 'package:type_model/classes/shapes.dart';
import 'package:type_model/enums/enums.dart';
import 'package:type_model/extension_types/extension_types.dart';
import 'package:type_model/extensions/extension_methods.dart';
import 'package:type_model/fields_accessors/fields_and_accessors.dart';
import 'package:type_model/generics/bounds.dart';
import 'package:type_model/generics/inference.dart';
import 'package:type_model/generics/inference_consumer.dart';
import 'package:type_model/generics/override_checking.dart';
import 'package:type_model/generics/variance.dart';
import 'package:type_model/mixins/mixins.dart';
import 'package:type_model/operators/operators.dart';
import 'package:type_model/records/records.dart';
import 'package:type_model/records/records_cross.dart';
import 'package:type_model/runtime_types/runtime_type_tests.dart';
import 'package:type_model/special_types/special_types.dart';

Future<void> main() async {
  final sections = <String, String>{
    'DART-CAN-TYPE-001 (classes)': describeClasses(),
    'DART-CAN-TYPE-002 (class modifiers)': describeModifiers(),
    'DART-CAN-TYPE-003 (mixins)': describeMixins(),
    'DART-CAN-TYPE-004 (enums)': describeEnums(),
    'DART-CAN-TYPE-005 (extension methods)': describeExtensions(),
    'DART-CAN-TYPE-006 (extension types)': describeExtensionTypes(),
    'DART-CAN-TYPE-007 (type aliases)': describeAliases(),
    'DART-CAN-TYPE-008 (records)': describeRecords(),
    'DART-CAN-TYPE-008 (cross-library records)': describeCrossLibraryRecords(),
    'DART-CAN-TYPE-009 (special types)': await describeSpecialTypes(),
    'DART-CAN-TYPE-010 (runtime type tests)': describeRuntimeTypes(),
    'DART-CAN-TYPE-011 (fields and accessors)': describeFieldsAndAccessors(),
    'DART-CAN-TYPE-012 (operators)': describeOperators(),
    'DART-CAN-GEN-001 (generic bounds)': describeBounds(),
    'DART-CAN-GEN-002 (inference)': describeInference(),
    'DART-CAN-GEN-002 (cross-library inference)':
        describeCrossLibraryInference(),
    'DART-CAN-GEN-003 (variance)': describeVariance(),
    'DART-CAN-GEN-004 (override checking)': describeOverrideChecking(),
  };

  stdout.writeln('type-model vm-jit');
  for (final entry in sections.entries) {
    stdout.writeln('== ${entry.key} ==');
    stdout.writeln('  ${entry.value}');
  }
}
