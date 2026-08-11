/// Native `Isolate.spawnUri` fixture. `spawnUri` loading arbitrary Dart
/// source is only exercised on the `vm-jit` context; an
/// ahead-of-time-compiled executable has no source compiler available to
/// load a sibling script by URI.
library;

import 'dart:io';
import 'dart:isolate';

/// Spawns [spawn_uri_worker.dart] by URI and returns its reply.
Future<String> spawnWorkerByUri() async {
  final workerUri = Platform.script.resolve(
    '../lib/isolates/spawn_uri_worker.dart',
  );
  final receivePort = ReceivePort();
  await Isolate.spawnUri(workerUri, ['fixture-arg'], receivePort.sendPort);
  final result = await receivePort.first;
  receivePort.close();
  return result as String;
}
