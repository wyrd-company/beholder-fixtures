library;

// Explicit `dart:core hide` removes the core `Duration` name so this library
// can declare its own local `Duration` without a name collision.
import 'dart:core' hide Duration;

/// A local declaration shadowing the (now-hidden) core `Duration` name.
class Duration {
  const Duration(this.totalUnits);

  final int totalUnits;

  @override
  String toString() => 'local-duration:$totalUnits';
}

String describeLocalDuration() => const Duration(5).toString();
