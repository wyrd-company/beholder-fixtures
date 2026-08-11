/// Isolate spawning and message fixtures: `Isolate.run`, `Isolate.spawn`,
/// ports, result/error/exit handling, and pause/resume/kill, all on
/// native targets.
library;

import 'dart:async';
import 'dart:isolate';

import 'package:async_and_isolates/isolates/isolate_entry_points.dart';

/// Runs [computeSquare] in a disposable isolate via [Isolate.run] and
/// returns its result; the isolate is spawned and shut down for you.
Future<int> runComputeSquareViaIsolateRun(int value) {
  return Isolate.run(() => computeSquare(value));
}

/// Spawns an isolate at the top-level entry point, exchanges one message
/// over a [ReceivePort]/[SendPort] pair, and returns the reply.
Future<int> spawnTopLevelEntryPointAndReceive() async {
  final receivePort = ReceivePort();
  await Isolate.spawn(topLevelEntryPoint, receivePort.sendPort);
  final result = await receivePort.first;
  receivePort.close();
  return result as int;
}

/// Spawns an isolate at the static entry point and returns its reply,
/// the class-based counterpart to [spawnTopLevelEntryPointAndReceive].
Future<String> spawnStaticEntryPointAndReceive() async {
  final receivePort = ReceivePort();
  await Isolate.spawn(
    IsolateEntryPoints.staticEntryPoint,
    receivePort.sendPort,
  );
  final result = await receivePort.first;
  receivePort.close();
  return result as String;
}

/// Spawns an isolate that exits via [Isolate.exit], delivering its final
/// message as part of exiting.
Future<String> spawnExitingEntryPointAndReceive() async {
  final receivePort = ReceivePort();
  await Isolate.spawn(exitingEntryPoint, receivePort.sendPort);
  final result = await receivePort.first;
  receivePort.close();
  return result as String;
}

/// Spawns an isolate that always throws and captures the description
/// delivered to its `onError` port.
Future<String> spawnFailingEntryPointAndCaptureError() async {
  final errorPort = ReceivePort();
  await Isolate.spawn(
    failingEntryPoint,
    errorPort.sendPort,
    onError: errorPort.sendPort,
  );
  final errorMessage = await errorPort.first;
  errorPort.close();
  return (errorMessage as List<Object?>).first as String;
}

/// Spawns an isolate that exits normally and observes its `onExit`
/// notification, which delivers `null` for a plain (non-`Isolate.exit`)
/// completion.
Future<bool> spawnAndObserveNormalExit() async {
  final receivePort = ReceivePort();
  final exitPort = ReceivePort();
  await Isolate.spawn(
    topLevelEntryPoint,
    receivePort.sendPort,
    onExit: exitPort.sendPort,
  );
  await receivePort.first;
  receivePort.close();
  final exitMessage = await exitPort.first;
  exitPort.close();
  return exitMessage == null;
}

/// Confirms that mutating [isolateLocalCounter] inside a spawned isolate
/// never affects the value observed in this, the spawning, isolate,
/// because isolates share no mutable state.
Future<(int, int)> confirmNoSharedMutableState() async {
  final before = isolateLocalCounter;
  final spawnedValue = await spawnTopLevelEntryPointAndReceive();
  final after = isolateLocalCounter;
  return (spawnedValue, after - before);
}

/// Spawns a periodically-ticking isolate, pauses it, confirms no further
/// ticks arrive while paused, resumes it, observes another tick, then
/// kills it. Returns `(countBeforePause, countWhilePaused, finalCount)`.
Future<(int, int, int)> pauseResumeAndKill() async {
  final receivePort = ReceivePort();
  final isolate = await Isolate.spawn(countingEntryPoint, receivePort.sendPort);
  final events = <int>[];
  final subscription = receivePort.listen((message) {
    events.add(message as int);
  });

  await _waitUntil(() => events.isNotEmpty);
  final countBeforePause = events.length;
  final resumeCapability = isolate.pause();

  await Future<void>.delayed(const Duration(milliseconds: 30));
  final countWhilePaused = events.length;

  isolate.resume(resumeCapability);
  await _waitUntil(() => events.length > countWhilePaused);

  isolate.kill(priority: Isolate.immediate);
  await subscription.cancel();
  receivePort.close();

  return (countBeforePause, countWhilePaused, events.length);
}

Future<void> _waitUntil(bool Function() condition) async {
  while (!condition()) {
    await Future<void>.delayed(const Duration(milliseconds: 1));
  }
}
