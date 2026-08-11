/// Generic and function variance, matching [DART-CAN-GEN-003]: class
/// covariance, function parameter contravariance, return covariance, and a
/// mutable generic upcast with an inserted runtime write check.
library;

class Animal2 {
  const Animal2(this.name);

  final String name;
}

class Dog2 extends Animal2 {
  const Dog2(super.name);
}

class Cat2 extends Animal2 {
  const Cat2(super.name);
}

/// Class (use-site) covariance: a `List<Dog2>` is usable where
/// `List<Animal2>` is expected.
List<Animal2> viewAsAnimals(List<Dog2> dogs) => dogs;

typedef AnimalTransformer = Animal2 Function(Dog2 input);

/// A wider parameter type (`Animal2` accepts any `Dog2` argument):
/// function-parameter contravariance.
Animal2 handlesAnyAnimal(Animal2 input) => Animal2('handled: ${input.name}');

/// A narrower return type (`Dog2` is an `Animal2`): function return
/// covariance.
Dog2 producesOnlyDogs(Dog2 input) => Dog2('bred: ${input.name}');

String describeVariance() {
  final dogs = <Dog2>[Dog2('Rex'), Dog2('Fido')];
  final animalsView = viewAsAnimals(dogs);

  // A mutable generic upcast: `upcast` and `dogs` refer to the same list,
  // but `upcast`'s static type is `List<Animal2>`.
  final List<Animal2> upcast = dogs;

  var writeCheckTriggered = false;
  try {
    // Statically valid against `List<Animal2>.add`, but the underlying
    // list is actually a `List<Dog2>`: the language's inserted runtime
    // write check rejects this write.
    upcast.add(Cat2('Whiskers'));
  } on TypeError {
    writeCheckTriggered = true;
  }

  // A genuinely valid write through the same upcast reference.
  upcast.add(Dog2('Buddy'));

  final AnimalTransformer wider = handlesAnyAnimal;
  final AnimalTransformer narrower = producesOnlyDogs;

  return 'animalsView=${animalsView.map((a) => a.name).toList()} '
      'writeCheckTriggered=$writeCheckTriggered dogsAfter=${dogs.length} '
      'widerResult=${wider(Dog2('Milo')).name} '
      'narrowerResult=${narrower(Dog2('Nova')).name}';
}
