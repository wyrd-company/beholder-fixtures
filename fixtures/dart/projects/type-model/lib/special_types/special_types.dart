/// Special types, matching [DART-CAN-TYPE-009]: `Object?`, `Object`,
/// `dynamic`, `void`, `Never`, `Null`, and `FutureOr<T>` in assignments,
/// calls, returns, promotion, and reachability.
library;

import 'dart:async';

Object? maybeAnything;
Object definitelySomething = 'something';
dynamic anythingGoes = 42;

void logNothing() {}

Never throwAlways(String message) => throw StateError(message);

Null explicitNull() => null;

FutureOr<int> futureOrValue(bool useFuture) {
  return useFuture ? Future<int>.value(7) : 7;
}

Future<String> describeSpecialTypes() async {
  final buffer = StringBuffer();

  // `Object?` accepts null; flow promotion to `Object` after a null check.
  // Promotion applies to local variables (not top-level fields), so the
  // top-level value is copied into a local first.
  maybeAnything = 'hello';
  final Object? maybeLocal = maybeAnything;
  if (maybeLocal != null) {
    final Object promoted = maybeLocal;
    buffer.writeln('promoted=$promoted');
  }

  buffer.writeln('definitelySomething=$definitelySomething');

  // `dynamic` permits any call without static checking, resolved at
  // runtime.
  anythingGoes = anythingGoes + 1;
  buffer.writeln('anythingGoes=$anythingGoes');

  logNothing();
  buffer.writeln('void call completed');

  // A `Never`-returning helper: reachability analysis knows no code after
  // its call site executes normally, so the catch is the only way out.
  try {
    throwAlways('always throws');
  } on StateError catch (e) {
    buffer.writeln('caught from Never source: ${e.message}');
  }

  buffer.writeln('explicitNull=${explicitNull()}');

  final awaitedFromValue = await futureOrValue(false);
  final awaitedFromFuture = await futureOrValue(true);
  buffer.writeln(
    'FutureOr resolved: value=$awaitedFromValue future=$awaitedFromFuture',
  );

  return buffer.toString();
}
