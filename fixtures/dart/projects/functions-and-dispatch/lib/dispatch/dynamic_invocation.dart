/// Dynamic invocation through a `dynamic`-typed receiver,
/// `Function.apply` with positional and symbol-keyed named arguments,
/// and a `noSuchMethod`-based forwarding proxy that satisfies an
/// interface without declaring its members directly.
library;

abstract interface class Greeter {
  String greet(String name, {String honorific});
}

class DirectGreeter implements Greeter {
  @override
  String greet(String name, {String honorific = 'Ms.'}) =>
      'Hello, $honorific $name';
}

/// A dynamic call: [receiver] is typed `dynamic`, so `greet` is
/// resolved at runtime rather than checked against a static interface.
String invokeDynamically(dynamic receiver, String name) {
  return receiver.greet(name, honorific: 'Dr.') as String;
}

int sumNamed(int a, int b, {int bonus = 0}) => a + b + bonus;

/// Invokes [sumNamed] through `Function.apply`, supplying positional
/// arguments as a list and the named `bonus` argument keyed by a
/// `Symbol` literal.
int applySumNamed() {
  return Function.apply(sumNamed, <int>[1, 2], <Symbol, int>{#bonus: 10})
      as int;
}

/// A forwarding proxy that satisfies [Greeter] entirely through
/// `noSuchMethod`. It declares no concrete `greet` implementation;
/// Dart permits a class implementing an interface to omit concrete
/// members when it overrides `noSuchMethod`, dispatching every
/// interface call dynamically instead.
class ForwardingGreeter implements Greeter {
  ForwardingGreeter(this._target);

  final Greeter _target;

  @override
  dynamic noSuchMethod(Invocation invocation) {
    if (invocation.memberName == #greet) {
      final name = invocation.positionalArguments[0] as String;
      final honorific =
          invocation.namedArguments[#honorific] as String? ?? 'Ms.';
      return _target.greet(name, honorific: honorific);
    }
    return super.noSuchMethod(invocation);
  }
}

/// Calls [ForwardingGreeter.greet] through its declared [Greeter]
/// interface type; the call reaches `noSuchMethod` because no concrete
/// `greet` member exists on [ForwardingGreeter].
String greetThroughForwarder(Greeter target, String name) {
  final Greeter forwarder = ForwardingGreeter(target);
  return forwarder.greet(name, honorific: 'Captain');
}
