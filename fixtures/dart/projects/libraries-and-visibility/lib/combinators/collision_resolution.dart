library;

// Both `collision_a.dart` and `collision_b.dart` declare a top-level
// `label()`. `show`/`hide` filters the import namespaces so only one
// `label()` reaches this library, resolving the collision.
import 'collision_a.dart' show label;
import 'collision_b.dart' hide label;

String describeCollisionResolution() => '${label()}/${otherLabel()}';
