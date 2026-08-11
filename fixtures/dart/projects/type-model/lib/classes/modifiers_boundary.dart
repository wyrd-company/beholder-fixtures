/// The library-boundary half of [DART-CAN-TYPE-002]: extends, implements,
/// and mixes in `modifiers_core.dart`'s modified classes and mixin from a
/// different library than where they are declared.
library;

import 'modifiers_core.dart';

/// Extending a `base` class from a different library requires the subclass
/// to be `base`, `final`, or `sealed`; combined here with applying a
/// `base mixin` across the same boundary.
base class Dog extends Animal with Swimmer {
  Dog(super.name);

  @override
  String speak() => '${super.speak()} (loudly)';
}

/// Implementing an `interface` class's interface from a different library.
class LoudSound implements Sound {
  @override
  String describe() => 'a loud sound';
}

/// Extending an `abstract base class` from a different library; the
/// subclass must again be `base`, `final`, or `sealed`.
base class Car extends AbstractVehicle {
  Car(super.model);

  @override
  String startEngine() => 'vroom';
}

/// Implementing an `abstract interface class` from a different library.
class Panel implements Describable {
  @override
  String describe() => 'a panel';
}

/// The `mixin class` [Flyer] used both as an ordinary superclass...
class Glider extends Flyer {
  String glide() => 'gliding';
}

/// ...and as a mixin, both from outside its declaring library.
class Plane with Flyer {
  String cruise() => 'cruising';
}

String describeModifiers() {
  final dog = Dog('Rex');
  final lock = Lock(1234);

  return 'dogSpeak=${dog.speak()} dogSwim=${dog.swimReport()} '
      'loudSound=${LoudSound().describe()} '
      'car=${Car('Sedan').describeVehicle()} '
      'panel=${Panel().describe()} glider=${Glider().glide()} '
      'plane=${Plane().cruise()} lock=${lock.describeLock()} '
      'shape2a=${describeShape2(Circle2(2))} '
      'shape2b=${describeShape2(Square2(3))} '
      'mathHelper=${MathHelpers.doubleValue(21)}';
}
