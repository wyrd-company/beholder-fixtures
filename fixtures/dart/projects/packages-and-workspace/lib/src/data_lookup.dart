import 'dart:convert';
import 'dart:io';
import 'dart:isolate';

/// Looks up `src/data/greeting.json`, bundled under this package's `lib/`
/// root, by its `package:` URI rather than a root-relative file path. This
/// resolves through the generated package configuration
/// (DART-CAN-PKG-004), so it reaches the data file regardless of which
/// package root the caller runs from — contrast with
/// `tool/report_tool.dart`, which looks up a file relative to its own
/// `tool/` root instead.
Future<String> loadGreeting() async {
  final dataUri = Uri.parse('package:signal_console/src/data/greeting.json');
  final resolved = await Isolate.resolvePackageUri(dataUri);
  if (resolved == null) {
    throw StateError(
      'unable to resolve $dataUri through the package configuration',
    );
  }
  final contents = await File.fromUri(resolved).readAsString();
  final decoded = jsonDecode(contents) as Map<String, Object?>;
  return decoded['greeting'] as String;
}
