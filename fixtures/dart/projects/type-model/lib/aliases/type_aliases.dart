/// Type aliases, matching [DART-CAN-TYPE-007]: legacy function typedef,
/// modern function alias, generalized class and type alias, generic
/// bounds, a record alias, and constructor access through an alias.
library;

// Legacy function typedef syntax.
typedef LegacyPredicate = bool Function(int value);

// Modern function-type alias (functionally identical, current syntax).
typedef ModernPredicate = bool Function(int value);

class Slot<T extends Object> {
  const Slot(this.value);

  final T value;

  factory Slot.wrapped(T value) => Slot(value);
}

// A generalized alias for a fully-applied generic class.
typedef IntSlot = Slot<int>;

// A generic alias with its own type parameter and bound.
typedef BoundedSlot<T extends num> = Slot<T>;

// A record type alias.
typedef Coordinates = (double lat, double lng);

bool isPositive(int value) => value > 0;

String describeAliases() {
  final LegacyPredicate legacy = isPositive;
  final ModernPredicate modern = isPositive;

  // Constructor access through an alias: both the unnamed and named
  // constructors are reachable via `IntSlot`.
  final unnamed = IntSlot(42);
  final named = IntSlot.wrapped(7);

  final boundedSlot = BoundedSlot<double>(3.14);

  const Coordinates origin = (0.0, 0.0);

  return 'legacy(5)=${legacy(5)} modern(-5)=${modern(-5)} '
      'unnamed=${unnamed.value} named=${named.value} '
      'bounded=${boundedSlot.value} origin=$origin';
}
