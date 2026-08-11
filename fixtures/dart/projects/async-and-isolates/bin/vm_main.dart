import 'dart:async';
import 'dart:io';

import 'package:async_and_isolates/checks/check_support.dart';
import 'package:async_and_isolates/futures/future_pipeline.dart';
import 'package:async_and_isolates/generators/generator_pipeline.dart';
import 'package:async_and_isolates/isolates/isolate_checks.dart';
import 'package:async_and_isolates/isolates/spawn_uri_launcher.dart';
import 'package:async_and_isolates/streams/stream_modes.dart';
import 'package:async_and_isolates/zones/zone_demo.dart';

Future<void> main() async {
  await _runFutures();
  _runGeneratorsSync();
  await _runGeneratorsAsync();
  await _runStreams();
  await _runZones();
  await _runIsolates();
  stdout.writeln('vm-jit async-and-isolates checks passed');
}

Future<void> _runFutures() async {
  expectEqual(
    await callTracedComputationAndObservePrefix(3),
    7,
    'callTracedComputationAndObservePrefix',
  );
  expectEqual(await returnPlainValue(4), 8, 'returnPlainValue');
  expectEqual(await returnNestedFuture(4), 12, 'returnNestedFuture');
  expectEqual(await maybeAsyncDouble(5), 10, 'maybeAsyncDouble sync');
  expectEqual(
    await maybeAsyncDouble(Future<int>.value(5)),
    10,
    'maybeAsyncDouble async',
  );
  expectEqual(
    await sumAwaitedInLoop([
      Future<int>.value(1),
      Future<int>.value(2),
      Future<int>.value(3),
    ]),
    6,
    'sumAwaitedInLoop',
  );
  expectEqual(
    await withFinallyCleanup(shouldThrow: false),
    'completed',
    'withFinallyCleanup ok',
  );
  final failed = await withFinallyCleanup(shouldThrow: true);
  if (!failed.startsWith('caught:')) {
    fail('withFinallyCleanup error', failed);
  }
}

void _runGeneratorsSync() {
  generatorTraceLog.clear();
  final iterable = lazyCount(3);
  if (generatorTraceLog.isNotEmpty) {
    fail('lazyCount laziness', 'trace populated before iteration');
  }
  expectList(iterable.toList(), [0, 1, 2], 'lazyCount values');
  expectList(generatorTraceLog, [
    'sync computed 0',
    'sync computed 1',
    'sync computed 2',
  ], 'lazyCount trace');

  expectList(lazyCountTwice(2).toList(), [0, 1, 0, 1], 'lazyCountTwice');

  generatorTraceLog.clear();
  var threw = false;
  try {
    throwingSyncGenerator().toList();
  } on StateError {
    threw = true;
  }
  if (!threw) {
    fail('throwingSyncGenerator', 'did not throw');
  }
  expectList(generatorTraceLog, ['sync finally'], 'throwingSyncGenerator');
}

Future<void> _runGeneratorsAsync() async {
  expectList(await lazyTicks(3).toList(), [0, 1, 2], 'lazyTicks values');
  expectList(await lazyTicksTwice(2).toList(), [0, 1, 0, 1], 'lazyTicksTwice');

  generatorTraceLog.clear();
  var threw = false;
  try {
    await throwingAsyncGenerator().toList();
  } on StateError {
    threw = true;
  }
  if (!threw) {
    fail('throwingAsyncGenerator', 'did not throw');
  }
  expectList(generatorTraceLog, ['async finally'], 'throwingAsyncGenerator');

  generatorTraceLog.clear();
  expectEqual(await takeFirstAndCancel(), 0, 'takeFirstAndCancel');
  await Future<void>.delayed(const Duration(milliseconds: 20));
  if (!generatorTraceLog.contains('async cancel finally')) {
    fail('cancelableTicks finally', generatorTraceLog.join(','));
  }
}

Future<void> _runStreams() async {
  final secondListenerResult = await secondListenerFailsOnSingleSubscription();
  if (!secondListenerResult.startsWith('caught:')) {
    fail('secondListenerFailsOnSingleSubscription', secondListenerResult);
  }

  final broadcast = broadcastCounterController(3);
  final (firstList, secondList) = await collectFromTwoBroadcastListeners(
    broadcast.stream,
  );
  expectList(firstList, [0, 1, 2], 'broadcast listener 1');
  expectList(secondList, [0, 1, 2], 'broadcast listener 2');

  final errorObservation = await observeDataThenError(
    broadcastCounterController(2).stream,
  );
  if (!errorObservation.startsWith('data=')) {
    fail('observeDataThenError', errorObservation);
  }

  expectList(
    await collectTransformedViaAwaitFor(singleSubscriptionCounter(5)),
    [0, 20, 40],
    'collectTransformedViaAwaitFor',
  );
  expectList(await collectDoubled(singleSubscriptionCounter(3)), [
    0,
    2,
    4,
  ], 'collectDoubled');
  expectList(await pauseThenResume(singleSubscriptionCounter(3)), [
    0,
    1,
    2,
  ], 'pauseThenResume');
  expectEqual(
    await cancelAfterTwoEvents(singleSubscriptionCounter(5)),
    2,
    'cancelAfterTwoEvents',
  );
}

Future<void> _runZones() async {
  expectList(await observeMicrotaskBeforeEvent(), [
    'microtask',
    'event',
  ], 'observeMicrotaskBeforeEvent');

  final fired = Completer<void>();
  fireAndForget(fired.complete);
  await fired.future;

  final intercepted = await runGuarded(throwFromUnawaitedFuture);
  if (intercepted is! StateError) {
    fail('runGuarded', '$intercepted');
  }

  expectEqual(
    runWithZoneLocalValue('vm-main-zone', readZoneLocalValue),
    'vm-main-zone',
    'runWithZoneLocalValue',
  );
  expectEqual(readZoneLocalValue(), 'root', 'readZoneLocalValue outside zone');
  expectEqual(
    bindCallbackAcrossZones(),
    'bound-zone',
    'bindCallbackAcrossZones',
  );
}

Future<void> _runIsolates() async {
  await runIsolateSpawningChecks();

  final spawnUriResult = await spawnWorkerByUri();
  if (!spawnUriResult.contains('fixture-arg')) {
    fail('spawnWorkerByUri', spawnUriResult);
  }

  await runSendableDataChecks();
}
