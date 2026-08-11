/// An entry-point reachability pragma: [dynamicOnlyHandler] is reached
/// only indirectly, by name, through [dispatchByName]'s dispatch
/// table, so nothing in this library calls it directly by its Dart
/// identifier. The `vm:entry-point` pragma tells the ahead-of-time
/// compiler's tree shaker to keep it reachable regardless of whether a
/// direct call site exists.
library;

@pragma('vm:entry-point')
String dynamicOnlyHandler(String input) => 'handled:$input';

String fallbackHandler(String input) => 'fallback:$input';

final Map<String, String Function(String)> _handlersByName =
    <String, String Function(String)>{
      'dynamic-only': dynamicOnlyHandler,
      'fallback': fallbackHandler,
    };

/// Looks up and invokes a handler purely by its string name.
String dispatchByName(String handlerName, String input) {
  final handler = _handlersByName[handlerName];
  if (handler == null) {
    throw ArgumentError.value(handlerName, 'handlerName', 'unknown handler');
  }
  return handler(input);
}
