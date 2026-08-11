import 'dart:io';

import 'package:signal_console/signal_console.dart';

/// Named executable (`signal-console` in `pubspec.yaml`'s `executables:`
/// mapping), invoked with `dart run` and positional arguments
/// (DART-CAN-PKG-008). Also the entry point compiled to a native
/// ahead-of-time executable for the `native-aot` build context.
Future<void> main(List<String> arguments) async {
  final app = ConsoleApp();
  stdout.writeln(await app.report(arguments));
}
