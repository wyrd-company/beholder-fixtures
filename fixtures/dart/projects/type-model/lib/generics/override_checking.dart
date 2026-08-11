/// Override checking and `covariant`, matching [DART-CAN-GEN-004]: valid
/// return covariance, parameter compatibility, optional and named
/// additions, and a deliberately narrowed parameter with `covariant`; a
/// call through a supertype causing a runtime check; generic substitution;
/// setter or field covariance; covariance across multiple interfaces.
library;

class Animal3 {
  const Animal3(this.name);

  final String name;
}

class Dog3 extends Animal3 {
  const Dog3(super.name);
}

class Base4 {
  Animal3 reproduce(Animal3 mate) => Animal3('offspring of ${mate.name}');

  void feed(Animal3 food, {int amount = 1, String? note}) {}
}

/// Valid return covariance ([reproduce] narrows the return type) and
/// parameter compatibility with an optional named addition.
class DogBreeder extends Base4 {
  @override
  Dog3 reproduce(Animal3 mate) => Dog3('puppy of ${mate.name}');

  @override
  void feed(Animal3 food, {int amount = 1, String? note, bool treat = false}) {}
}

class Base5 {
  void accept(Animal3 animal) {}
}

/// A deliberately narrowed parameter using `covariant`, opting into a
/// runtime check because the narrower type cannot be statically verified
/// against the base signature.
class DogOnlyAccepter extends Base5 {
  @override
  void accept(covariant Dog3 animal) {}
}

class Container2<T> {
  T store(T value) => value;
}

/// Generic substitution: the override's parameter and return types are
/// `Container2<int>`'s substitution of `T` with `int`.
class IntContainer extends Container2<int> {
  @override
  int store(int value) => value * 2;
}

class AnimalPen {
  set resident(Animal3 animal) {}
}

/// Setter covariance: narrowing a setter's parameter also requires
/// `covariant`.
class DogPen extends AnimalPen {
  @override
  set resident(covariant Dog3 animal) {}
}

abstract class Feeder1 {
  void give(Animal3 item);
}

abstract class Feeder2 {
  void give(Animal3 item);
}

/// Covariance across multiple interfaces: one `covariant` narrowing
/// simultaneously satisfies both implemented interfaces.
class DogFeeder implements Feeder1, Feeder2 {
  @override
  void give(covariant Dog3 item) {}
}

String describeOverrideChecking() {
  final breeder = DogBreeder();
  final Dog3 pup = breeder.reproduce(const Dog3('Rex'));
  breeder.feed(const Dog3('Fido'), treat: true);

  final Base5 accepterAsBase = DogOnlyAccepter();
  accepterAsBase.accept(const Dog3('Fido'));

  var covariantCheckTriggered = false;
  try {
    // Statically valid against `Base5.accept`, but `DogOnlyAccepter`'s
    // override narrowed the parameter with `covariant`: calling through
    // the supertype reference with a non-`Dog3` argument triggers the
    // inserted runtime check.
    accepterAsBase.accept(const Animal3('Generic Animal'));
  } on TypeError {
    covariantCheckTriggered = true;
  }

  final intContainer = IntContainer();

  final AnimalPen penAsBase = DogPen();
  var setterCheckTriggered = false;
  try {
    // Statically valid against `AnimalPen.resident=`, but `DogPen`'s
    // override narrowed the setter's parameter with `covariant`.
    penAsBase.resident = const Animal3('Generic Animal');
  } on TypeError {
    setterCheckTriggered = true;
  }
  penAsBase.resident = const Dog3('Buddy');

  final dogFeeder = DogFeeder()..give(const Dog3('Nova'));

  return 'pup=${pup.name} covariantCheckTriggered=$covariantCheckTriggered '
      'storedDoubled=${intContainer.store(21)} '
      'setterCheckTriggered=$setterCheckTriggered '
      'dogFeederRuntimeType=${dogFeeder.runtimeType}';
}
