// @dart=2.19
// Before Dart 3.7, `_` is an ordinary identifier: a single, real, readable
// binding rather than a non-binding wildcard. Contrast with
// `modern_wildcards.dart`, where repeated `_` bindings create no binding and
// cannot be read.
library fixture.wildcards.legacy;

int legacySingleUnderscoreBinding(int seed) {
  final _ = seed + 1;
  return _;
}
