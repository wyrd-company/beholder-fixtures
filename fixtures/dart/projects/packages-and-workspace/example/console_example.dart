import 'package:signal_console/signal_console.dart';

/// Example entry library (DART-CAN-PKG-002's `example/` root), reachable
/// only within its own root: it imports the package façade by `package:`
/// URI like any external consumer would, but nothing outside `example/`
/// imports this file back.
Future<void> main() async {
  final app = ConsoleApp();
  print(await app.report(const ['7.5', '3.25']));
}
