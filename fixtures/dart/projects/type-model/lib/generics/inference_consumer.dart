/// The cross-library half of [DART-CAN-GEN-002]: this library depends on
/// `inference.dart`'s inferred `String` and `List<int>` top-level types
/// without either declaration re-stating them.
library;

import 'inference.dart' as base;

String describeCrossLibraryInference() {
  final shout = base.upwardInferredTopLevel.toUpperCase();
  final total = base.downwardList.fold<int>(0, (a, b) => a + b);
  return 'shout=$shout total=$total';
}
