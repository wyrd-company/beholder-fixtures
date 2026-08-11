import 'dart:io';

import 'package:null_safety_flow_patterns/null_safety_flow_patterns.dart';

void main() {
  final sections = <String, List<String>>{
    'DART-CAN-NULL-001 (nullable-types)': describeNullableTypes(),
    'DART-CAN-NULL-002 (flow-promotion)': describeFlowPromotion(),
    'DART-CAN-NULL-003 (definite-assignment-and-late)':
        describeDefiniteAssignmentAndLate(),
    'DART-CAN-NULL-004 (null-aware-selection)': describeNullAwareSelection(),
    'DART-CAN-FLOW-001 (statements-loops-labels-reachability)':
        describeStatementsLoopsAndReachability(),
    'DART-CAN-FLOW-002 (switch-forms-and-exhaustiveness)':
        describeSwitchFormsAndExhaustiveness(),
    'DART-CAN-FLOW-003 (pattern-taxonomy)': describePatternTaxonomy(),
    'DART-CAN-FLOW-004 (pattern-contexts-and-scope)':
        describePatternContextsAndScope(),
    'DART-CAN-FLOW-005 (exceptions-and-stack-flow)':
        describeExceptionsAndStackFlow(),
    'DART-CAN-COLL-001 (collection-literal-kinds-and-inference)':
        describeCollectionLiteralKindsAndInference(),
    'DART-CAN-COLL-002 (collection-control-flow-and-spreads)':
        describeCollectionControlFlowAndSpreads(),
    'DART-CAN-COLL-003 (null-aware-collection-elements)':
        describeNullAwareCollectionElements(),
  };

  stdout.writeln('null-safety-flow-patterns vm-jit');
  for (final entry in sections.entries) {
    stdout.writeln('== ${entry.key} ==');
    for (final line in entry.value) {
      stdout.writeln('  $line');
    }
  }
}
