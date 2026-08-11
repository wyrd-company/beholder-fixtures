/// Process, filesystem, and environment observations on native targets,
/// matching DART-CAN-PLAT-008. Every native target (VM JIT, native AOT)
/// supports `dart:io`; `js` and `wasm` do not, which is why this library is
/// reachable only from `platform_report_native.dart`'s conditional branch
/// and this project's native-only entry points.
library;

import 'dart:io';

/// Joins path segments using this platform's separator
/// ([Platform.pathSeparator]), a native-target-only concern.
String joinPath(List<String> segments) => segments.join(Platform.pathSeparator);

/// Reads an environment variable through `dart:io`'s
/// [Platform.environment].
String? readEnvironmentVariable(String name) => Platform.environment[name];

/// Writes [contents] to a scratch file under the system temporary
/// directory, reads it back asynchronously, then removes the scratch
/// directory — exercising async file I/O without mutating any tracked
/// project source.
Future<String> writeReadDeleteScratchFile(String contents) async {
  final scratchDir = await Directory.systemTemp.createTemp(
    'platforms-and-interop-',
  );
  final scratchFile = File(joinPath([scratchDir.path, 'scratch.txt']));
  try {
    await scratchFile.writeAsString(contents);
    return await scratchFile.readAsString();
  } finally {
    await scratchDir.delete(recursive: true);
  }
}

/// Invokes the `echo` process and returns its exit code, demonstrating
/// process invocation and exit on a native target.
Future<int> runEchoProcess(String message) async {
  final result = await Process.run('echo', [message]);
  return result.exitCode;
}
