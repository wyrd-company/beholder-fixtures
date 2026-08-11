/// Event queue, unawaited future, and zone fixtures: documented
/// microtask/event ordering, `unawaited`, a guarded zone, a zone-local
/// value, an intercepted asynchronous error, and callbacks bound to
/// zones.
library;

import 'dart:async';

/// Records observed ordering for the microtask-versus-event
/// demonstration.
final List<String> zoneTraceLog = <String>[];

/// Schedules a microtask and a zero-delay timer event, in that order,
/// and records which one actually runs first. Dart's documented
/// event-loop contract drains every pending microtask before the next
/// event-queue task runs, so the microtask always wins even though the
/// timer has zero delay.
Future<List<String>> observeMicrotaskBeforeEvent() {
  zoneTraceLog.clear();
  final completer = Completer<List<String>>();
  Timer(Duration.zero, () {
    zoneTraceLog.add('event');
    completer.complete(List<String>.of(zoneTraceLog));
  });
  scheduleMicrotask(() => zoneTraceLog.add('microtask'));
  return completer.future;
}

/// Fires an async operation without awaiting it, marking that intent
/// explicitly with [unawaited] rather than leaving a bare, unawaited
/// expression statement.
void fireAndForget(void Function() onComplete) {
  unawaited(Future<void>.delayed(Duration.zero, onComplete));
}

/// Runs [body] inside a guarded zone that intercepts asynchronous errors
/// escaping unawaited futures, rather than letting them reach the top
/// level uncaught, and returns the intercepted error.
Future<Object?> runGuarded(void Function() body) {
  final completer = Completer<Object?>();
  runZonedGuarded(body, (error, stackTrace) {
    if (!completer.isCompleted) {
      completer.complete(error);
    }
  });
  return completer.future;
}

/// Throws from an unawaited future; when run inside [runGuarded], the
/// zone's error handler intercepts the error instead of it reaching an
/// uncaught top level.
void throwFromUnawaitedFuture() {
  unawaited(Future<void>(() => throw StateError('zone-intercepted error')));
}

/// The zone-local key used by [readZoneLocalValue] and
/// [bindCallbackAcrossZones].
const Symbol zoneTagKey = #zoneTag;

/// Runs [body] inside a zone carrying a zone-local value under
/// [zoneTagKey].
R runWithZoneLocalValue<R>(String tag, R Function() body) {
  return runZoned(body, zoneValues: {zoneTagKey: tag});
}

/// Reads the current zone's zone-local tag, defaulting to `'root'` when
/// none is set.
String readZoneLocalValue() {
  return (Zone.current[zoneTagKey] as String?) ?? 'root';
}

/// Binds a callback while inside a tagged zone, then invokes it after
/// returning to the root zone. The callback still observes the zone it
/// was bound in, not the zone it is invoked from.
String bindCallbackAcrossZones() {
  late final void Function() bound;
  final observed = <String>[];
  runWithZoneLocalValue('bound-zone', () {
    bound = Zone.current.bindCallback(() {
      observed.add(readZoneLocalValue());
    });
  });

  bound();
  return observed.single;
}
