/// Simple and enhanced enums, matching [DART-CAN-TYPE-004]: values with
/// fields, methods, const constructor arguments, an interface, a mixin, and
/// synthesized members; a generic enhanced enum.
library;

enum Simple { red, green, blue }

abstract interface class Reported {
  String describe();
}

mixin Chatty {
  String chatPrefix() => 'says:';
}

/// An enhanced enum: values carry fields set through const constructor
/// arguments, an implemented interface, a mixed-in mixin, and a method.
enum Planet with Chatty implements Reported {
  mercury(massKg: 3.3e23, radiusKm: 2439.7),
  venus(massKg: 4.87e24, radiusKm: 6051.8),
  earth(massKg: 5.97e24, radiusKm: 6371.0);

  const Planet({required this.massKg, required this.radiusKm});

  final double massKg;
  final double radiusKm;

  double get gravity =>
      6.674e-11 * massKg / (radiusKm * 1000 * radiusKm * 1000);

  @override
  String describe() => '${chatPrefix()} $name (index=$index)';
}

/// A generic enhanced enum: each value supplies its own type argument.
enum Wrapped<T> {
  intWrapper<int>(0),
  stringWrapper<String>('');

  const Wrapped(this.defaultValue);

  final T defaultValue;
}

String describeEnums() {
  final planetDescriptions = [for (final p in Planet.values) p.describe()];

  return 'simpleValues=${Simple.values} planets=$planetDescriptions '
      'earthGravity=${Planet.earth.gravity.toStringAsFixed(2)} '
      'wrappedInt=${Wrapped.intWrapper.defaultValue} '
      'wrappedString=${Wrapped.stringWrapper.defaultValue.isEmpty} '
      'synthesized=(${Simple.red.name},${Simple.red.index},'
      '${Simple.values.length}) '
      'switchResult=${switch (Simple.blue) {
        Simple.red => 'r',
        Simple.green => 'g',
        Simple.blue => 'b',
      }}';
}
