/// Reachability and tree-shaking demonstrations shared by every compiled
/// entry point, matching DART-CAN-PLAT-003: the same valid behavior must
/// hold under VM JIT and native AOT, alongside deliberately unreachable
/// source and an entry-point preservation pragma.
library;

/// Never called from this project's entry points. A backend that performs
/// tree shaking (native AOT, `js`, `wasm`) is free to omit it from its
/// compiled output; the VM JIT, which does not tree-shake, always retains
/// it. See `diagnostics/non_portable_observations.dart` for the tree-shaken
/// boundary this creates.
String unreachableGreeting() => 'never reached';

/// Invoked only through the dynamic, string-keyed dispatch table in
/// [dynamicEntryPoints] rather than through a direct Dart call site — the
/// pattern `@pragma('vm:entry-point')` exists to support. An AOT tree
/// shaker that traces only static call graphs would otherwise be free to
/// discard a declaration reached solely through a runtime lookup (an
/// embedder callback, a plugin host, or a reflection-driven dispatch
/// table).
@pragma('vm:entry-point')
String preservedForDynamicInvocation() => 'preserved for dynamic invocation';

/// A runtime-built dispatch table modeling invocation from outside this
/// project's static call graph.
final Map<String, String Function()> dynamicEntryPoints = {
  'preserved': preservedForDynamicInvocation,
};

/// Behavior shared by every compiled target: looks up and invokes the
/// preserved entry point through [dynamicEntryPoints], identically under
/// VM JIT and native AOT.
String describeReachability() {
  final entryPoint = dynamicEntryPoints['preserved'];
  if (entryPoint == null) {
    throw StateError('preserved entry point missing');
  }
  return entryPoint();
}
