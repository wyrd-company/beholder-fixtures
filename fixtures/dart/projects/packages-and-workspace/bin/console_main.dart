import 'dart:io';

import 'package:signal_console/signal_console.dart';

/// Named executable (`signal-console` in `pubspec.yaml`'s `executables:`
/// mapping), invoked with `dart run signal_console:console_main` and
/// positional arguments (DART-CAN-PKG-008). `bin/admin_tool_main.dart` is
/// the entry point compiled to a native ahead-of-time executable for the
/// `native-aot` build context.
Future<void> main(List<String> arguments) async {
  final app = ConsoleApp();
  stdout.writeln(await app.report(arguments));
}
