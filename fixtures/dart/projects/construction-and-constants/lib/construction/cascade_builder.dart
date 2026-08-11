/// Cascade fixtures for [DART-CAN-OBJ-005]: `..` and `?..` sections built
/// from calls, assignments, and index sections; the cascade expression's
/// result as the original receiver; a first null-aware section that
/// short-circuits later sections; and a nested cascade.
library;

class Cart {
  Cart(this.label);

  String label;
  final List<String> _items = <String>[];

  void add(String item) => _items.add(item);

  String operator [](int index) => _items[index];

  void operator []=(int index, String value) => _items[index] = value;

  List<String> get items => List<String>.unmodifiable(_items);
}

class Counter {
  Counter(this.label);

  String label;
  int hits = 0;

  void ping() => hits += 1;
}

Counter? _maybeCounter(bool present) => present ? Counter('probe') : null;

/// Builds a [Cart] using call, assignment, and index-section cascades, then
/// confirms the cascade expression evaluates to the original receiver.
(Cart built, bool cascadeReturnsReceiver) buildCart() {
  final cart = Cart('groceries');
  final result = cart
    ..add('apples')
    ..add('bread')
    ..label = 'weekly groceries'
    ..[0] = 'green apples';
  return (result, identical(result, cart));
}

/// A cascade whose first section is null-aware: when the receiver is null,
/// every later section in the same cascade is skipped too.
int? nullShortingCascadeHits(bool present) {
  final counter = _maybeCounter(present);
  final result = counter
    ?..ping()
    ..ping();
  return result?.hits;
}

/// A cascade section whose argument is itself built from a nested cascade.
Cart nestedCascadeCart() {
  final basket = Cart('basket')
    ..add('outer-item')
    ..[0] =
        (Cart('nested')
              ..add('nested-item')
              ..add('nested-item-2'))
            .items
            .join(',');
  return basket;
}

List<String> describeCascades() {
  final (built, returnsReceiver) = buildCart();
  final presentHits = nullShortingCascadeHits(true);
  final absentHits = nullShortingCascadeHits(false);
  final nested = nestedCascadeCart();

  return <String>[
    'Cascade-built cart items: ${built.items}, label=${built.label}',
    'Cascade expression evaluates to the original receiver: $returnsReceiver',
    'Present receiver: both cascade sections ran, hits=$presentHits',
    'Null receiver: first null-aware section short-circuits the rest, '
        'result=$absentHits',
    'Nested cascade result: ${nested.items}',
  ];
}
