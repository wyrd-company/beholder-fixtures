/// The cross-library half of [DART-CAN-TYPE-008]: a record produced by
/// `records.dart` and a record produced locally, sharing the same
/// `({int x, int y})` shape with no shared nominal declaration, are
/// structurally interchangeable.
library;

import 'records.dart' as records;

({int x, int y}) makeNamedElsewhere() => (x: 3, y: 4);

String describeCrossLibraryRecords() {
  final local = makeNamedElsewhere();
  final imported = records.makeNamed();

  // Both values share exactly the same record type despite originating
  // from different libraries with no shared type declaration.
  final combined = <({int x, int y})>[local, imported];

  return 'crossLibraryShapes=$combined';
}
