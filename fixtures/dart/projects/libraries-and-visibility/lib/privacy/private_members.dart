library;

/// A private top-level type.
class _PrivateType {
  const _PrivateType(this.tag);

  final String tag;
}

class Holder {
  int _value = 0;

  void _increment() => _value++;
}

class Peer {
  // Two classes in one library can access each other's private members.
  String readHolderValue(Holder holder) {
    holder._increment();
    return 'holder-value:${holder._value}';
  }
}

class WithPrivateConstructor {
  WithPrivateConstructor._(this.tag);

  final String tag;

  factory WithPrivateConstructor.create(String tag) =>
      WithPrivateConstructor._(tag);
}

/// A private extension.
extension _PrivateFormatter on int {
  String describePrivately() => 'n=$this';
}

String _secretName() => 'from-private-members';

String describePrivateMembersSecret() => _secretName();

String describePrivateType() => const _PrivateType('demo').tag;

String describePrivateConstructor() =>
    WithPrivateConstructor.create('demo').tag;

String describePrivateExtension() => 3.describePrivately();
