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

/// Carries no Dart-source reference anywhere in this project: it is never
/// torn off, called, or stored in a table this project's own code reads.
/// `@pragma('vm:entry-point')` models the real case this pragma exists
/// for — a declaration entered only from outside the Dart call graph
/// entirely (an embedder, a native host, or generated binding code
/// invoking it by name through the VM's C API) — so native AOT's tree
/// shaker, which can only trace static Dart references, must be told
/// explicitly to retain it. Without the pragma, native AOT would be free
/// to discard it exactly like [unreachableGreeting]; this project takes
/// no Dart call site to it, so that difference is not misrepresented as a
/// dynamic Dart lookup this project does not actually perform.
@pragma('vm:entry-point')
String preservedForExternalInvocation() => 'preserved for external invocation';

/// Behavior shared by every compiled target: identical arithmetic and
/// string formatting under VM JIT and native AOT.
String describeReachability() {
  final squares = List.generate(5, (i) => i * i);
  return 'reachability squares: ${squares.join(',')}';
}
