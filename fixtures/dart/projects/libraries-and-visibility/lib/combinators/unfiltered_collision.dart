library;

// Both `collision_a.dart` and `collision_b.dart` declare a top-level
// `label()`. Importing both here with no `show`/`hide` filtering is valid:
// two different declarations sharing one imported name are ambiguous only
// when that name is actually used. This file never references `label`, so
// only `uniqueA()` (from `collision_a.dart`) and `otherLabel()` (from
// `collision_b.dart`), neither of which collides, are used.
import 'collision_a.dart';
import 'collision_b.dart';

String describeUnfilteredCollision() => '${uniqueA()}/${otherLabel()}';
