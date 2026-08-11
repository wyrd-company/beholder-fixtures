// @dart=2.19
/// Legacy library pinned below the package default language version.
library legacy_consumer;

import 'package:configuration_and_versions/language/modern_library.dart';

/// Pair modeled with a class because records are unavailable at 2.19.
class Pair {
  const Pair(this.first, this.second);

  final int first;
  final int second;
}

/// Imports a dependency library that keeps its own resolved language version.
Pair pairFromOrigin() {
  final Coordinate origin = originCoordinate();
  return Pair(origin.$1, origin.$2);
}
