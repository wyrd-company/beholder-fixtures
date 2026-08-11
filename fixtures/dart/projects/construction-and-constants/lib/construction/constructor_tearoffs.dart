/// Constructor tear-off fixtures for [DART-CAN-OBJ-004]: `C.new`, a named
/// constructor tear-off, a prefixed tear-off, an instantiated generic
/// constructor tear-off, const-context tear-off identity, and alias-mediated
/// constructor access.
library;

import 'point.dart';
import 'point.dart' as geo;
import 'shape_factory.dart';

/// A type alias mediating access to [Point]'s constructors.
typedef PointAlias = Point;

/// `C.new` as a plain function value.
final Point Function(double, double) unnamedTearOff = Point.new;

/// A named constructor torn off as a function value.
final Point Function() namedTearOff = Point.origin;

/// A tear-off reached through an import prefix.
final Point Function(double, double) prefixedTearOff = geo.Point.new;

/// An instantiated generic constructor tear-off: the type argument is fixed
/// at the tear-off site.
final Box<int> Function(int) instantiatedGenericTearOff = Box<int>.new;

/// A tear-off reached through a type alias rather than the class name.
final Point Function() aliasedTearOff = PointAlias.origin;

/// Two syntactically distinct tear-off expressions for the same named
/// constructor, each assigned in a constant context.
const Point Function() originTearOffA = Point.origin;
const Point Function() originTearOffB = Point.origin;

List<String> describeConstructorTearoffs() {
  final unnamed = unnamedTearOff(1, 2);
  final named = namedTearOff();
  final prefixed = prefixedTearOff(3, 4);
  final boxed = instantiatedGenericTearOff(7);
  final aliased = aliasedTearOff();

  return <String>[
    'Point.new tear-off invoked: $unnamed',
    'Point.origin named tear-off invoked: $named',
    'geo.Point.new prefixed tear-off invoked: $prefixed',
    'Box<int>.new instantiated generic tear-off invoked: value=${boxed.value}',
    'PointAlias.origin alias-mediated tear-off invoked: $aliased',
    'const Point.origin tear-offs canonicalize in a const context: '
        'sameInstance=${identical(originTearOffA, originTearOffB)}',
  ];
}
