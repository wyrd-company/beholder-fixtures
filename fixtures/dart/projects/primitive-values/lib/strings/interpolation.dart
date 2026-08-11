/// String interpolation, raw-string interpolation suppression, and
/// const-context interpolation.
library;

const name = 'fixture';
const count = 3;

const interpolatedIdentifier = 'hello $name';
const interpolatedExpression = 'count plus one is ${count + 1}';
final interpolatedMethodCall = 'uppercase is ${name.toUpperCase()}';

/// A raw string containing a literal `$name`; raw strings suppress
/// interpolation entirely, so no substitution happens.
const rawSuppressesInterpolation = r'literal $name stays as text';

/// Interpolation evaluated in a `const` context: every interpolated
/// expression here is itself a compile-time constant.
const constInterpolation = 'const: $name/$count';

List<String> describeInterpolation() => <String>[
  'interpolatedIdentifier=$interpolatedIdentifier',
  'interpolatedExpression=$interpolatedExpression',
  'interpolatedMethodCall=$interpolatedMethodCall',
  'rawSuppressesInterpolation=$rawSuppressesInterpolation',
  'constInterpolation=$constInterpolation',
];
