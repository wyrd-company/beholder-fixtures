/// Structural and generic function types, callable-object coercion,
/// the untyped `Function` type, and parameter/return variance in
/// function-type assignability.
library;

/// A structural function type used as a typedef.
typedef BinaryOp = int Function(int a, int b);

/// A structural function type matching a unary operation.
typedef UnaryOp = int Function(int value);

/// A generic function type: the type parameter belongs to the function
/// type itself, independent of any enclosing generic declaration.
typedef Transformer = T Function<T>(T value);

int addStructural(int a, int b) => a + b;

/// Assigns the top-level function to a variable of the structural
/// function type [BinaryOp].
BinaryOp selectAddStructural() => addStructural;

T identityTransform<T>(T value) => value;

/// Assigns a generic top-level function to a variable of the generic
/// function type [Transformer].
Transformer selectIdentityTransformer() => identityTransform;

/// A callable object: a class with a `call()` method implicitly
/// coerces to a matching function type wherever one is expected.
class Multiplier {
  const Multiplier(this.factor);

  final int factor;

  int call(int value) => value * factor;
}

/// Returns the callable [Multiplier] instance coerced to [UnaryOp].
UnaryOp coerceCallableToFunctionType(Multiplier multiplier) => multiplier;

/// Accepts the untyped `Function` type, which admits any function
/// value regardless of its specific signature.
String describeAnyFunction(Function fn) => fn.runtimeType.toString();

class Animal {
  const Animal(this.name);

  final String name;
}

class Dog extends Animal {
  const Dog(String name) : super(name);
}

/// A function accepting the supertype [Animal] and returning the more
/// specific subtype [Dog].
Dog reviveAsDog(Animal animal) => Dog(animal.name);

/// A function type accepting the subtype [Dog] and returning the wider
/// supertype [Animal].
typedef AnimalHandler = Animal Function(Dog dog);

/// [reviveAsDog] has type `Dog Function(Animal)`, which is a subtype of
/// [AnimalHandler] (`Animal Function(Dog)`): its parameter type
/// ([Animal]) is wider than required ([Dog]) — contravariance — and
/// its return type ([Dog]) is narrower than required ([Animal]) —
/// covariance. Both directions must hold for the assignment below to
/// be valid.
AnimalHandler pickHandler() => reviveAsDog;
