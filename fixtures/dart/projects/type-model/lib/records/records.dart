/// Records, matching [DART-CAN-TYPE-008]: positional, named, singleton
/// positional, nested, const, generic, return, destructuring, and
/// cross-library record shapes; structural subtyping; synthetic getters;
/// record equality; named-field order versus names.
library;

(int, String) makePositional() => (1, 'one');

({int x, int y}) makeNamed() => (x: 1, y: 2);

/// A singleton positional record: the trailing comma is required to
/// distinguish it from a parenthesized expression.
(int,) makeSingleton() => (42,);

(int, (String, bool)) makeNested() => (1, ('inner', true));

const (int, int) constPair = (10, 20);

(T, T) duplicate<T>(T value) => (value, value);

String describeRecords() {
  final positional = makePositional();
  final named = makeNamed();
  final singleton = makeSingleton();
  final nested = makeNested();

  // Destructuring via record patterns.
  final (a, b) = positional;
  final (:x, :y) = named;

  final generic = duplicate<String>('twice');

  // Structural subtyping: record types are covariant per field, so a record
  // whose field types are proper subtypes of a wider record type's field
  // types (`int` vs `num` here) is itself a subtype of that wider type,
  // with no explicit conversion.
  final ({num x, num y}) widened = named;

  // Synthetic getters: field names/positions become getters on the record.
  final positionalGetter = positional.$1;
  final namedGetter = named.x;

  // Record equality is structural.
  final equalRecords = (1, 'one') == positional;

  // Named-field order does not affect equality: only names and values
  // matter.
  final reordered = (y: 2, x: 1);
  final orderIndependentEquality = reordered == named;

  return 'positional=$positional named=$named singleton=$singleton '
      'nested=$nested constPair=$constPair destructured=($a,$b) '
      'namedDestructured=(x:$x,y:$y) generic=$generic '
      'widened=$widened positionalGetter=$positionalGetter '
      'namedGetter=$namedGetter equalRecords=$equalRecords '
      'orderIndependentEquality=$orderIndependentEquality';
}
