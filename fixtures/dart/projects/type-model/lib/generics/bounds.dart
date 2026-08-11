/// Generic declarations and bounds, matching [DART-CAN-GEN-001]: generic
/// classes, mixins, extensions, extension types, aliases, functions,
/// methods, and constructors; upper, dependent, and F-bounds; explicit and
/// inferred arguments; the raw form; `extends Object?`. Generic extension
/// types and generic aliases are also demonstrated in
/// `extension_types/extension_types.dart` and `aliases/type_aliases.dart`.
library;

/// An upper-bounded generic class.
class NumericBox<T extends num> {
  const NumericBox(this.value);

  final T value;
}

/// `extends Object?` explicitly admits nullable type arguments.
class AnyBox<T extends Object?> {
  const AnyBox(this.value);

  final T value;
}

/// A dependent bound: the second type parameter's bound refers to the
/// first.
class PairedBox<T, U extends T> {
  const PairedBox(this.primary, this.secondary);

  final T primary;
  final U secondary;
}

/// An F-bound: `T` must itself be comparable to `T`.
abstract class SelfComparable<T extends SelfComparable<T>> {
  int compareToSelf(T other);
}

class Rank extends SelfComparable<Rank> {
  Rank(this.value);

  final int value;

  @override
  int compareToSelf(Rank other) => value.compareTo(other.value);
}

/// A generic mixin.
mixin Countable<T> {
  final List<T> _items = <T>[];

  void track(T item) => _items.add(item);

  int get trackedCount => _items.length;
}

class Tracker<T> with Countable<T> {}

/// A generic extension.
extension IterableSummary<T> on Iterable<T> {
  String summarize() => 'count=$length first=${isEmpty ? null : first}';
}

/// A generic top-level function.
T identity<T>(T value) => value;

/// A generic class with a generic factory constructor.
class Repository<T> {
  Repository();

  final List<T> _items = <T>[];

  void add(T item) => _items.add(item);

  T? firstOrNull() => _items.isEmpty ? null : _items.first;

  /// A generic method: `R` is this method's own type parameter, distinct
  /// from the enclosing class's `T`.
  List<R> mapTo<R>(R Function(T item) transform) =>
      _items.map(transform).toList();

  factory Repository.of(Iterable<T> items) {
    final repo = Repository<T>();
    for (final item in items) {
      repo.add(item);
    }
    return repo;
  }
}

String describeBounds() {
  final numeric = NumericBox<int>(5);
  final anyBox = AnyBox<String?>(null);
  final paired = PairedBox<num, int>(1.5, 2);
  final rank = Rank(3);
  final tracker = Tracker<String>()
    ..track('a')
    ..track('b');

  final explicitIdentity = identity<int>(7);
  final inferredIdentity = identity('inferred');

  // The raw (unparameterized) form: the type argument defaults to `T`'s
  // bound.
  final Repository raw = Repository();
  raw.add('anything');

  final repo = Repository<int>.of(<int>[1, 2, 3]);
  final mapped = repo.mapTo<String>((item) => 'item-$item');

  return 'numeric=${numeric.value} anyBox=${anyBox.value} '
      'paired=(${paired.primary},${paired.secondary}) '
      'rankCompare=${rank.compareToSelf(Rank(1))} '
      'trackedCount=${tracker.trackedCount} '
      'explicitIdentity=$explicitIdentity inferredIdentity=$inferredIdentity '
      'rawRepoFirst=${raw.firstOrNull()} repoOfFirst=${repo.firstOrNull()} '
      'mapped=$mapped summary=${<int>[1, 2, 3].summarize()}';
}
