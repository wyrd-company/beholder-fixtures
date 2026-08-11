/// Fields and accessors, matching [DART-CAN-TYPE-011]: instance, static,
/// and top-level fields; `final`, `late`, `late final`, static `const`, and
/// abstract fields; explicit getters and setters; a getter and setter
/// inherited from different supertypes; implementing a field with computed
/// accessors; overriding one accessor half; a final collection remaining
/// mutable.
library;

int topLevelField = 1;
final String topLevelFinal = 'top-level-final';
const double topLevelConst = 3.14;

class Holder {
  Holder.withLate(this.instanceField) {
    lateField = 'computed-late';
    lateFinalField = 'computed-late-final';
  }

  int instanceField;
  static int staticField = 0;
  static const String staticConstField = 'static-const';
  late String lateField;
  late final String lateFinalField;

  /// The field reference is immutable (`final`), but the list it points to
  /// remains mutable.
  final List<int> mutableContents = <int>[1, 2, 3];
}

abstract class HasAbstractField {
  abstract int abstractField;
}

class ConcreteField implements HasAbstractField {
  @override
  int abstractField = 10;
}

// A getter and a setter inherited from two different supertypes.
class BaseWithGetter {
  final int _v = 5;

  int get value => _v;
}

mixin SetterMixin {
  int _mixinStored = 0;

  set value(int v) => _mixinStored = v;

  int get mixinStoredValue => _mixinStored;
}

class InheritsReadable extends BaseWithGetter with SetterMixin {}

class StoredTemperature {
  double celsius = 0;
}

/// Implements [StoredTemperature]'s stored field as a computed accessor
/// pair instead of a stored field.
class ComputedTemperature implements StoredTemperature {
  double _fahrenheit = 32;

  @override
  double get celsius => (_fahrenheit - 32) * 5 / 9;

  @override
  set celsius(double value) => _fahrenheit = value * 9 / 5 + 32;
}

class Named2 {
  String _name = 'anonymous';

  String get name => _name;

  set name(String value) => _name = value;
}

/// Overrides only the getter half of an inherited accessor pair, leaving
/// the inherited setter untouched.
class ShoutingName extends Named2 {
  @override
  String get name => _name.toUpperCase();
}

String describeFieldsAndAccessors() {
  final holder = Holder.withLate(1)..instanceField = 2;
  holder.mutableContents.add(4);

  final concrete = ConcreteField();

  final inherited = InheritsReadable();
  inherited.value = 3;

  final computedTemp = ComputedTemperature()..celsius = 100;

  final shouting = ShoutingName()..name = 'quiet';

  return 'topLevelField=$topLevelField topLevelFinal=$topLevelFinal '
      'topLevelConst=$topLevelConst instanceField=${holder.instanceField} '
      'staticField=${Holder.staticField} '
      'staticConst=${Holder.staticConstField} '
      'lateField=${holder.lateField} lateFinalField=${holder.lateFinalField} '
      'mutableContents=${holder.mutableContents} '
      'abstractField=${concrete.abstractField} '
      'inheritedGetter=${inherited.value} '
      'inheritedSetterStored=${inherited.mixinStoredValue} '
      'computedTempCelsius=${computedTemp.celsius} '
      'shoutingName=${shouting.name}';
}
