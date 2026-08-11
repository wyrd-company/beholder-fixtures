/// Synchronous and asynchronous generator fixtures: `sync*`, `async*`,
/// `yield`, `yield*`, visible laziness, delegation, and error/finally
/// handling, contrasting iterable and stream behavior.
library;

import 'dart:async';

/// Records generator-body side effects to make laziness observable.
final List<String> generatorTraceLog = <String>[];

/// Lazily yields `0` through `n - 1`; nothing in the body runs until the
/// returned [Iterable] is actually iterated.
Iterable<int> lazyCount(int n) sync* {
  for (var i = 0; i < n; i++) {
    generatorTraceLog.add('sync computed $i');
    yield i;
  }
}

/// Delegates to [lazyCount] twice via `yield*`.
Iterable<int> lazyCountTwice(int n) sync* {
  yield* lazyCount(n);
  yield* lazyCount(n);
}

/// Yields once, then throws. The `finally` block still runs because the
/// thrown error propagates out through the generator's own call frame.
Iterable<int> throwingSyncGenerator() sync* {
  try {
    yield 1;
    throw StateError('throwingSyncGenerator failure');
  } finally {
    generatorTraceLog.add('sync finally');
  }
}

/// Asynchronously yields `0` through `n - 1`. Every `yield` in an
/// `async*` body suspends through the event loop, unlike the purely
/// synchronous pull-based iteration of `sync*`.
Stream<int> lazyTicks(int n) async* {
  for (var i = 0; i < n; i++) {
    generatorTraceLog.add('async computed $i');
    yield i;
  }
}

/// Delegates to [lazyTicks] twice via `yield*`.
Stream<int> lazyTicksTwice(int n) async* {
  yield* lazyTicks(n);
  yield* lazyTicks(n);
}

/// Yields once, then throws; the `finally` block runs as the stream
/// controller backing this `async*` body tears down.
Stream<int> throwingAsyncGenerator() async* {
  try {
    yield 1;
    throw StateError('throwingAsyncGenerator failure');
  } finally {
    generatorTraceLog.add('async finally');
  }
}

/// Ticks forever until its subscription is cancelled. Cancellation
/// resumes this generator solely to run its `finally` block, a cleanup
/// protocol streams support that plain iterables do not.
Stream<int> cancelableTicks() async* {
  try {
    var i = 0;
    while (true) {
      yield i;
      i += 1;
    }
  } finally {
    generatorTraceLog.add('async cancel finally');
  }
}

/// Cancels a subscription to [cancelableTicks] right after the first
/// event and returns that event's value.
Future<int> takeFirstAndCancel() {
  final completer = Completer<int>();
  late final StreamSubscription<int> subscription;
  subscription = cancelableTicks().listen((value) {
    completer.complete(value);
    subscription.cancel();
  });
  return completer.future;
}
