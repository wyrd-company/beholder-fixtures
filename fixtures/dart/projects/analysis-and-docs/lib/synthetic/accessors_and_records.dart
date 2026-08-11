/// Field accessors, record getters, and enum synthetic members.
library;

// Field accessors: a field induces a getter and, if writable, a setter.
class FieldAccessors {
  FieldAccessors(this.label, this.count);

  final String label;
  int count;

  String get computedLabel => 'lab:$label';
  set computedLabel(String value) {}
}

// Record getters: positional and named fields expose synthetic getters.
(String first, int second) makePositionalRecord(String a, int b) => (a, b);

({String label, int count}) makeNamedRecord(String label, int count) =>
    (label: label, count: count);

// Access via record getters.
String useRecordGetters() {
  final rec = (label: 'Bracket', count: 2);
  return rec.label;
}

// Enum with synthesized members: `values`, `index`, `name`, `hashCode` etc.
enum WorkshopRole {
  assembler,
  inspector,
  packer;

  String title() => 'role:$name';
}

// Observable via iteration over `values` and member access.
List<String> roleNames() => WorkshopRole.values.map((r) => r.name).toList();

int roleIndex(WorkshopRole role) => role.index;
