/// Stream consumption and subscription-mode fixtures: `await for`,
/// single-subscription and broadcast streams, a controller,
/// transformations, error events, cancellation, and pause/resume.
library;

import 'dart:async';

/// A single-subscription stream backed by a [StreamController], emitting
/// `0` through `n - 1` and then closing.
Stream<int> singleSubscriptionCounter(int n) {
  final controller = StreamController<int>();
  scheduleMicrotask(() async {
    for (var i = 0; i < n; i++) {
      controller.add(i);
    }
    await controller.close();
  });
  return controller.stream;
}

/// A broadcast stream controller supporting more than one listener; it
/// emits data, then an error event, then closes.
StreamController<int> broadcastCounterController(int n) {
  final controller = StreamController<int>.broadcast();
  scheduleMicrotask(() async {
    for (var i = 0; i < n; i++) {
      controller.add(i);
    }
    controller.addError(StateError('broadcast error event'));
    await controller.close();
  });
  return controller;
}

/// A custom transformer that doubles each value, exercised alongside the
/// `.map()`/`.where()` chain in [collectTransformedViaAwaitFor].
final StreamTransformer<int, int> doublingTransformer =
    StreamTransformer<int, int>.fromHandlers(
      handleData: (value, sink) => sink.add(value * 2),
    );

/// Attempting a second `.listen()` on a single-subscription stream fails
/// at runtime with a [StateError]; returns the caught error's message.
Future<String> secondListenerFailsOnSingleSubscription() async {
  final stream = singleSubscriptionCounter(3);
  final subscription = stream.listen((_) {});
  try {
    stream.listen((_) {});
    return 'no error';
  } on StateError catch (error) {
    return 'caught: ${error.message}';
  } finally {
    await subscription.cancel();
  }
}

/// Subscribes two independent listeners to the same broadcast stream and
/// returns the values each one observed.
Future<(List<int>, List<int>)> collectFromTwoBroadcastListeners(
  Stream<int> broadcast,
) async {
  final first = <int>[];
  final second = <int>[];
  final firstDone = Completer<void>();
  final secondDone = Completer<void>();
  final firstSub = broadcast.listen(
    first.add,
    onError: (Object _) {},
    onDone: firstDone.complete,
  );
  final secondSub = broadcast.listen(
    second.add,
    onError: (Object _) {},
    onDone: secondDone.complete,
  );
  await Future.wait([firstDone.future, secondDone.future]);
  await firstSub.cancel();
  await secondSub.cancel();
  return (first, second);
}

/// Listens for data values followed by an error event on a broadcast
/// stream and reports both once the error arrives.
Future<String> observeDataThenError(Stream<int> source) {
  final completer = Completer<String>();
  final seen = <int>[];
  late final StreamSubscription<int> subscription;
  subscription = source.listen(
    seen.add,
    onError: (Object error) {
      completer.complete('data=$seen error=$error');
      subscription.cancel();
    },
  );
  return completer.future;
}

/// Consumes a stream with `await for` after filtering and mapping it,
/// demonstrating stream transformations ahead of the consuming loop.
Future<List<int>> collectTransformedViaAwaitFor(Stream<int> source) async {
  final results = <int>[];
  final transformed = source
      .where((value) => value.isEven)
      .map((value) => value * 10);
  await for (final value in transformed) {
    results.add(value);
  }
  return results;
}

/// Consumes a stream through the custom [doublingTransformer].
Future<List<int>> collectDoubled(Stream<int> source) {
  return source.transform(doublingTransformer).toList();
}

/// Pauses a subscription after its first event, resumes it on the next
/// microtask, and returns every value observed in arrival order.
Future<List<int>> pauseThenResume(Stream<int> source) {
  final results = <int>[];
  final completer = Completer<List<int>>();
  late final StreamSubscription<int> subscription;
  subscription = source.listen((value) {
    results.add(value);
    if (results.length == 1) {
      subscription.pause();
      scheduleMicrotask(subscription.resume);
    }
  }, onDone: () => completer.complete(results));
  return completer.future;
}

/// Cancels a subscription right after its second event and reports how
/// many events it observed before cancellation.
Future<int> cancelAfterTwoEvents(Stream<int> source) {
  final completer = Completer<int>();
  var count = 0;
  late final StreamSubscription<int> subscription;
  subscription = source.listen((value) {
    count += 1;
    if (count == 2) {
      subscription.cancel();
      completer.complete(count);
    }
  });
  return completer.future;
}
