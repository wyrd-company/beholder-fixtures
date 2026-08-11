/// Mixins and mixin applications, matching [DART-CAN-TYPE-003]: `mixin`,
/// `on` constraints, multiple ordered applications, `super` calls, and a
/// named mixin application; later-mixin precedence; the same mixin over
/// different bases having different `super` targets.
library;

class Engine {
  String start() => 'engine starting';
}

class ElectricEngine extends Engine {
  @override
  String start() => 'silent ${super.start()}';
}

mixin Loggable {
  String log(String message) => '[log] $message';
}

class Logger with Loggable {}

/// An `on` constraint: [Turbo] can only be mixed into a subtype of
/// [Engine], because its `super.start()` call requires one.
mixin Turbo on Engine {
  String boost() => '${super.start()} + turbo boost';
}

/// Applying [Turbo] over two different base classes gives `super.start()`
/// two different targets: [Engine.start] and [ElectricEngine.start].
class TurboCar extends Engine with Turbo {}

class TurboElectricCar extends ElectricEngine with Turbo {}

mixin First {
  String identify() => 'first';
}

mixin Second {
  String identify() => 'second';
}

/// Multiple ordered mixin applications: [Second] is applied after [First],
/// so it wins for `identify()` (the later mixin takes precedence).
class Combined with First, Second {}

/// A named mixin application: a fixed combination of a superclass with a
/// mixin, declared with `=`.
class NamedTurboCar = Engine with Turbo;

String describeMixins() {
  return 'turboCar=${TurboCar().boost()} '
      'turboElectricCar=${TurboElectricCar().boost()} '
      'combined=${Combined().identify()} '
      'logger=${Logger().log('mixin demo')} '
      'namedTurboCar=${NamedTurboCar().boost()}';
}
