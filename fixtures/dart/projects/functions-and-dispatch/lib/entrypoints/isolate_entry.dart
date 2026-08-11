/// A top-level isolate entry-point function, torn off and passed to
/// `Isolate.spawn`, demonstrating the entry-point-signature shape this
/// project owns. Full isolate messaging mechanics — multiple spawn
/// strategies, sendable-data rules, pause/resume/kill — belong to the
/// async-and-isolates fixture project; this project exercises only the
/// entry-point tear-off itself.
library;

import 'dart:isolate';

/// An isolate entry point: a top-level function taking exactly one
/// message argument and returning `void`, the signature
/// `Isolate.spawn` requires.
void isolateEntryPoint(SendPort sendPort) {
  sendPort.send('isolate-entry-point-ran');
}

/// Tears off [isolateEntryPoint] and spawns it, returning the single
/// message it sends back.
Future<String> spawnIsolateEntryTearOff() async {
  final receivePort = ReceivePort();
  final entryTearOff = isolateEntryPoint;
  await Isolate.spawn(entryTearOff, receivePort.sendPort);
  final message = await receivePort.first as String;
  receivePort.close();
  return message;
}
