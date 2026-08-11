library;

// Multiple `_` parameters create no binding under the modern (3.7+)
// wildcards feature, so repeating `_` is not a duplicate-parameter error.
void wildcardParameters(int _, String _) {}

int wildcardLocalsAndPatterns(int value) {
  // Multiple `_` locals create no binding, so redeclaring `_` is legal.
  var _ = value * 2;
  var _ = value * 3;

  // A wildcard in a record-destructuring pattern position.
  final (first, _) = (value, value + 1);
  return first;
}

String wildcardCatch() {
  try {
    throw StateError('demo');
  } catch (_) {
    // The catch-clause wildcard creates no readable binding.
    return 'caught';
  }
}

class WildcardHolder {
  // A member `_` declaration remains a real, single declaration (a private
  // field named `_`), unlike a local or parameter wildcard.
  final int _ = 42;

  int read() => _;
}

// A top-level `_` declaration also remains a real, single declaration.
const _ = 99;

int useTopLevelWildcard() => _;

// The unnamed extension idiom: an extension with no name at all.
extension on num {
  String labelled() => 'n:$this';
}

String describeUnnamedExtension(num value) => value.labelled();
