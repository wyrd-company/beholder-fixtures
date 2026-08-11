import 'dart:io';

import 'package:functions_and_dispatch/checks/check_support.dart';
import 'package:functions_and_dispatch/dispatch/dispatch_resolution.dart';
import 'package:functions_and_dispatch/dispatch/dynamic_invocation.dart';
import 'package:functions_and_dispatch/entrypoints/isolate_entry.dart';
import 'package:functions_and_dispatch/entrypoints/reachability.dart';

/// A second, asynchronous entry library alongside the synchronous
/// `vm_main.dart`, both roots of this fixture project under the
/// default `vm-jit` context. It exercises dynamic invocation, dispatch
/// resolution, the isolate entry-point tear-off, and the
/// `vm:entry-point` reachability pragma.
Future<void> main(List<String> arguments) async {
  stdout.writeln('vm-jit async entry ran with ${arguments.length} arguments');
  _runDynamicInvocation();
  _runDispatchResolution();
  await _runIsolateEntry();
  _runReachability();
  stdout.writeln('vm-jit vm_async_main checks passed');
}

void _runDynamicInvocation() {
  expectEqual(
    invokeDynamically(DirectGreeter(), 'Ada'),
    'Hello, Dr. Ada',
    'invokeDynamically',
  );
  expectEqual(applySumNamed(), 13, 'applySumNamed');
  expectEqual(
    greetThroughForwarder(DirectGreeter(), 'Grace'),
    'Hello, Captain Grace',
    'greetThroughForwarder',
  );
}

void _runDispatchResolution() {
  expectEqual(virtualDispatch(Circle()), 'circle', 'virtualDispatch Circle');
  expectEqual(virtualDispatch(Shape()), 'shape', 'virtualDispatch Shape');
  expectEqual(staticDispatch(), 'a generic shape', 'staticDispatch');
  expectEqual(constructorDispatch().kind(), 'circle', 'constructorDispatch');
  expectEqual(
    extensionDispatch(Circle()),
    'extension-shape:Circle',
    'extensionDispatch resolves by static type',
  );
  expectEqual(
    extensionTypeDispatch(Circle()),
    'view:circle',
    'extensionTypeDispatch',
  );
}

Future<void> _runIsolateEntry() async {
  final message = await spawnIsolateEntryTearOff();
  expectEqual(message, 'isolate-entry-point-ran', 'spawnIsolateEntryTearOff');
}

void _runReachability() {
  expectEqual(
    dispatchByName('dynamic-only', 'x'),
    'handled:x',
    'dispatchByName dynamic-only',
  );
  expectEqual(
    dispatchByName('fallback', 'x'),
    'fallback:x',
    'dispatchByName fallback',
  );
}
