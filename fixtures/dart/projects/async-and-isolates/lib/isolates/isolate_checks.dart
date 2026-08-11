/// Isolate spawning, messaging, and sendability checks shared by both
/// the `vm-jit` and `native-aot` entry points. `spawnUri` is not
/// included here because it is only exercised on `vm-jit`.
library;

import 'package:async_and_isolates/checks/check_support.dart';
import 'package:async_and_isolates/isolates/isolate_spawning.dart';
import 'package:async_and_isolates/isolates/sendable_data.dart';

/// Runs every native isolate spawning/messaging demonstration:
/// `Isolate.run`, `Isolate.spawn` with top-level and static entry
/// points, exit/error handling, no-shared-mutable-state, and
/// pause/resume/kill.
Future<void> runIsolateSpawningChecks() async {
  expectEqual(
    await runComputeSquareViaIsolateRun(6),
    36,
    'runComputeSquareViaIsolateRun',
  );
  expectEqual(
    await spawnTopLevelEntryPointAndReceive(),
    5,
    'spawnTopLevelEntryPointAndReceive',
  );
  expectEqual(
    await spawnStaticEntryPointAndReceive(),
    'hello from static entry point',
    'spawnStaticEntryPointAndReceive',
  );
  expectEqual(
    await spawnExitingEntryPointAndReceive(),
    'final message via Isolate.exit',
    'spawnExitingEntryPointAndReceive',
  );

  final errorMessage = await spawnFailingEntryPointAndCaptureError();
  if (!errorMessage.contains('failingEntryPoint failure')) {
    fail('spawnFailingEntryPointAndCaptureError', errorMessage);
  }

  expectEqual(
    await spawnAndObserveNormalExit(),
    true,
    'spawnAndObserveNormalExit',
  );

  final (spawnedValue, delta) = await confirmNoSharedMutableState();
  expectEqual(spawnedValue, 5, 'confirmNoSharedMutableState spawnedValue');
  expectEqual(delta, 0, 'confirmNoSharedMutableState delta');

  final (beforePause, whilePaused, stillPaused, finalCount) =
      await pauseResumeAndKill();
  // `whilePaused` is deliberately not compared against `beforePause`:
  // `Isolate.pause()` takes effect only once the target receives the
  // request, so a tick already in flight may still arrive afterward, and
  // the accepted brief requires that host/message-ordering corner to
  // remain an observation rather than an assertion. Comparing the two
  // samples taken entirely within the paused window instead confirms
  // ticks stopped arriving once pausing had taken hold.
  final pauseTookEffect =
      beforePause >= 1 &&
      whilePaused == stillPaused &&
      finalCount > stillPaused;
  if (!pauseTookEffect) {
    fail(
      'pauseResumeAndKill',
      '$beforePause,$whilePaused,$stillPaused,$finalCount',
    );
  }
}

/// Runs every sendability demonstration: primitives and collections,
/// ports, immutable sharing, cyclic data, an unsendable value, and
/// `TransferableTypedData` transfer plus reuse failure.
Future<void> runSendableDataChecks() async {
  final echoedMap =
      await echoPrimitivesAndCollections() as Map<Object?, Object?>;
  expectEqual(echoedMap['int'], 7, 'echoPrimitivesAndCollections');
  expectEqual(await echoSendPort(), true, 'echoSendPort');
  expectEqual(
    await echoImmutableConstantTwiceAndCompareIdentity(),
    true,
    'echoImmutableConstantTwiceAndCompareIdentity',
  );
  expectEqual(await echoCyclicMap(), true, 'echoCyclicMap');

  final unsendableResult = await attemptSendUnsendableValue();
  if (!unsendableResult.startsWith('caught:')) {
    fail('attemptSendUnsendableValue', unsendableResult);
  }

  expectEqual(await transferTypedData(), 100, 'transferTypedData');

  final reuseResult = await materializeTransferableTwice();
  if (!reuseResult.startsWith('caught:')) {
    fail('materializeTransferableTwice', reuseResult);
  }
}
