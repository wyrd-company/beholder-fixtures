/// `Future`, `async`, and `await` fixtures: synchronous prefixes,
/// suspension, value/future return flattening, `FutureOr`, awaiting in
/// loops, and `try`/`finally`.
library;

import 'dart:async';

/// Records observed execution order for the synchronous-prefix and
/// suspension demonstrations.
final List<String> futureTraceLog = <String>[];

/// Runs its prefix synchronously up to the first `await`, then suspends
/// and resumes once the awaited future completes.
Future<int> tracedComputation(int seed) async {
  futureTraceLog.add('prefix start $seed');
  final doubled = seed * 2;
  futureTraceLog.add('prefix end $seed');
  final resumed = await Future<int>.value(doubled);
  futureTraceLog.add('resumed $resumed');
  return resumed + 1;
}

/// Calls [tracedComputation] and confirms its synchronous prefix already
/// ran before this function ever awaits the returned future.
Future<int> callTracedComputationAndObservePrefix(int seed) async {
  futureTraceLog.clear();
  final future = tracedComputation(seed);
  final prefixLength = futureTraceLog.length;
  final result = await future;
  return prefixLength == 2 ? result : -1;
}

/// Returns a plain, already-available value; `async` wraps it into a
/// `Future<int>` for the caller.
Future<int> returnPlainValue(int value) async {
  return value * 2;
}

/// Returns another future from within an `async` function; Dart flattens
/// the result to `Future<int>` rather than nesting `Future<Future<int>>`.
Future<int> returnNestedFuture(int value) async {
  return Future<int>.value(value * 3);
}

/// Accepts and returns `FutureOr<int>`, handling both the synchronous and
/// asynchronous shapes a caller may supply.
FutureOr<int> maybeAsyncDouble(FutureOr<int> input) {
  if (input is int) {
    return input * 2;
  }
  return input.then((value) => value * 2);
}

/// Awaits a mix of pending futures inside a loop, accumulating their
/// results in sequence.
Future<int> sumAwaitedInLoop(List<Future<int>> pending) async {
  var total = 0;
  for (final future in pending) {
    total += await future;
  }
  return total;
}

/// Demonstrates `try`/`finally` around an awaited operation. The finally
/// block runs whether the awaited future completes normally or with an
/// error caught by the surrounding `try`.
Future<String> withFinallyCleanup({required bool shouldThrow}) async {
  futureTraceLog.add('cleanup start');
  try {
    if (shouldThrow) {
      await Future<void>.error(StateError('withFinallyCleanup failure'));
    } else {
      await Future<void>.value();
    }
    return 'completed';
  } catch (error) {
    return 'caught: $error';
  } finally {
    futureTraceLog.add('cleanup finally');
  }
}
