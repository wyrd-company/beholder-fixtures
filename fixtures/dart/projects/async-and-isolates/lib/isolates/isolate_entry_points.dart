/// Top-level and static isolate entry points, plus the isolate-local
/// mutable state used to demonstrate that isolates share no memory.
library;

import 'dart:async';
import 'dart:isolate';

/// Mutable state private to whichever isolate is running this library.
/// Because isolates do not share memory, mutating this from a spawned
/// isolate never affects the value observed in another isolate.
int isolateLocalCounter = 0;

/// A top-level isolate entry point: mutates isolate-local state and
/// reports the result back over [sendPort].
void topLevelEntryPoint(SendPort sendPort) {
  isolateLocalCounter += 5;
  sendPort.send(isolateLocalCounter);
}

/// Groups the class-based alternative to a top-level entry point.
class IsolateEntryPoints {
  IsolateEntryPoints._();

  /// A static isolate entry point, the class-based counterpart to
  /// [topLevelEntryPoint].
  static void staticEntryPoint(SendPort sendPort) {
    sendPort.send('hello from static entry point');
  }
}

/// A plain top-level computation used by [Isolate.run] demonstrations.
int computeSquare(int value) => value * value;

/// Terminates itself via [Isolate.exit], delivering its final message as
/// part of exiting rather than sending then separately shutting down.
void exitingEntryPoint(SendPort sendPort) {
  Isolate.exit(sendPort, 'final message via Isolate.exit');
}

/// Always throws, used to demonstrate `onError` handling for a spawned
/// isolate.
void failingEntryPoint(SendPort sendPort) {
  throw StateError('failingEntryPoint failure');
}

/// Sends an increasing count on a fixed interval until killed, used by
/// pause/resume/kill demonstrations where pausing must take effect
/// between discrete events rather than mid-computation.
void countingEntryPoint(SendPort sendPort) {
  var count = 0;
  Timer.periodic(const Duration(milliseconds: 5), (timer) {
    count += 1;
    sendPort.send(count);
  });
}
