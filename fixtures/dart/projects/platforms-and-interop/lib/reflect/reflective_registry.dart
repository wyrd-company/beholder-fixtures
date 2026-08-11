/// Reflective discovery and invocation through `dart:mirrors`, matching
/// DART-CAN-PLAT-009. `dart:mirrors` is available only under VM JIT — it is
/// rejected outright by native AOT, `js`, and `wasm` compilation — so this
/// library is imported only from `bin/mirrors_main.dart`, a dedicated
/// JIT-only entry point never compiled to another target. Unlike
/// DART-CAN-PLAT-002's other native-only libraries, this isolation cannot
/// be expressed as a `dart.library.*` conditional import: no compile-time
/// condition distinguishes VM JIT from native AOT, since both take the
/// same native branch of that conditional. A separate, never-compiled
/// entry point is this project's isolation mechanism instead.
library;

import 'dart:mirrors';

/// Metadata attached to [ReflectiveTarget], readable through
/// [ClassMirror.metadata].
final class Marker {
  const Marker(this.label);
  final String label;
}

/// A generic class whose type argument is discoverable through
/// [ClassMirror.typeArguments], and which declares a private method
/// reachable only by name through reflective invocation in
/// [describeReflectively] — never through a direct Dart call site.
@Marker('reflective-target')
final class ReflectiveTarget<T> {
  ReflectiveTarget(this._value);

  final T _value;

  // ignore: unused_element
  T _describe() => _value;
}

/// Discovers [ReflectiveTarget]'s metadata, generic type argument, and
/// private `_describe` method through `dart:mirrors`, then invokes that
/// method reflectively.
String describeReflectively(ReflectiveTarget<int> target) {
  final instanceMirror = reflect(target);
  final classMirror = instanceMirror.type;

  final metadata = classMirror.metadata
      .map((declaration) => declaration.reflectee)
      .whereType<Marker>()
      .single;

  final typeArgument = classMirror.typeArguments.single;

  final invocation = instanceMirror.invoke(#_describe, const []);

  return 'label=${metadata.label} typeArgument=$typeArgument '
      'value=${invocation.reflectee}';
}
