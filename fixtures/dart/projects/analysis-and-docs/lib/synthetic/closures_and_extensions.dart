/// Closures and unnamed extensions for DART-CAN-DIAG-008.
library;

// Closure entities: lambda and tear-off create closure objects.
int Function(int) makeAdder(int base) =>
    (int x) => base + x;

String Function() makeGreeter(String name) =>
    () => 'hi $name';

// Named extension.
extension StringTruncate on String {
  String truncated(int max) => length <= max ? this : substring(0, max);
}

// Unnamed extension: no explicit name, still contributes members.
extension on int {
  int doubled() => this * 2;
}

// Unnamed generic extension example.
extension on List<String> {
  String joined() => join(',');
}

String useExtensions() {
  final s = 'workshop'.truncated(4);
  final d = 7.doubled();
  final j = ['a', 'b'].joined();
  final adder = makeAdder(3);
  return '$s:$d:$j:${adder(2)}';
}
