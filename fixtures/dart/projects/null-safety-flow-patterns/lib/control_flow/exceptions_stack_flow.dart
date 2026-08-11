/// DART-CAN-FLOW-005: exceptions and stack flow.
library;

class GeneralException implements Exception {
  final String message;

  GeneralException(this.message);
}

/// `throw` paired with a typed `catch`.
String describeTypedCatch() {
  try {
    throw GeneralException('boom');
  } on GeneralException catch (error) {
    return 'caught:${error.message}';
  }
}

/// A non-`Exception` object: Dart allows throwing any object, and an
/// untyped `catch` receives it unchanged.
String describeUntypedCatchOfNonException() {
  try {
    throw 'a raw string error';
  } catch (error) {
    return 'caught:$error (type=${error.runtimeType})';
  }
}

/// A `catch` clause with both an error and a stack-trace parameter.
String describeStackTraceParameter() {
  try {
    throw StateError('trace-me');
  } catch (error, stackTrace) {
    return 'caught:$error hasStack=${stackTrace.toString().isNotEmpty}';
  }
}

/// `rethrow` re-raises the caught error (preserving its original stack
/// trace) to an enclosing handler.
String describeRethrow() {
  try {
    try {
      throw FormatException('inner');
    } catch (_) {
      rethrow;
    }
  } on FormatException catch (error) {
    return 'rethrown-caught:${error.message}';
  }
}

/// Catch order: clauses are tried top-to-bottom, so the most specific `on`
/// clause that matches wins even when a broader clause below could also
/// match.
String describeCatchOrder(Object errorToThrow) {
  try {
    throw errorToThrow;
  } on FormatException catch (error) {
    return 'format:${error.message}';
  } on Exception catch (error) {
    return 'exception:$error';
  } catch (error) {
    return 'other:$error';
  }
}

/// A `finally` block's own `return` overrides the try block's `return`.
int describeFinallyOverridingReturn() {
  try {
    return 1;
  } finally {
    return 2;
  }
}

/// A `finally` block's own `return` overrides an in-flight `throw`,
/// suppressing propagation of the original error.
int describeFinallyOverridingThrow() {
  try {
    throw StateError('would have propagated');
  } finally {
    return 99;
  }
}

/// The synchronous side of the synchronous-versus-asynchronous error-flow
/// contrast: a synchronous `throw` is caught by an ordinary `catch` at the
/// point of the call.
String describeSynchronousErrorFlow() {
  try {
    throw StateError('synchronous failure');
  } catch (error) {
    return 'caught-sync:$error';
  }
}

Future<int> _asynchronousFailure() async {
  throw StateError('asynchronous failure');
}

/// The asynchronous side of the contrast: a `throw` inside a
/// `Future`-returning `async` function only reaches a `catch` once the
/// caller `await`s the call; the surrounding synchronous code does not
/// observe the error at the call site itself.
Future<String> describeAsynchronousErrorFlow() async {
  try {
    await _asynchronousFailure();
    return 'no-error';
  } catch (error) {
    return 'caught-async:$error';
  }
}

List<String> describeExceptionsAndStackFlow() {
  return <String>[
    'typedCatch=${describeTypedCatch()}',
    'untypedCatchOfNonException=${describeUntypedCatchOfNonException()}',
    'stackTraceParameter=${describeStackTraceParameter()}',
    'rethrow=${describeRethrow()}',
    'catchOrder(format)=${describeCatchOrder(FormatException('bad-format'))}',
    'catchOrder(exception)=${describeCatchOrder(GeneralException('general'))}',
    'catchOrder(other)=${describeCatchOrder('raw')}',
    'finallyOverridingReturn=${describeFinallyOverridingReturn()}',
    'finallyOverridingThrow=${describeFinallyOverridingThrow()}',
    'synchronousErrorFlow=${describeSynchronousErrorFlow()}',
  ];
}
