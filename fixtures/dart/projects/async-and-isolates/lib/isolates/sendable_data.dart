/// Sendability and transferable-data fixtures: primitives, collections,
/// ports, `TransferableTypedData`, immutable sharing, an unsendable
/// value, cyclic sendable data, and transfer-reuse failure.
library;

import 'dart:isolate';
import 'dart:typed_data';

/// Echoes back whatever sendable message it receives, used by every
/// demonstration below.
void echoEntryPoint(List<Object?> args) {
  final sendPort = args[0] as SendPort;
  final message = args[1];
  sendPort.send(message);
}

/// Sends a mix of primitives and a nested `List`/`Set` collection
/// through an isolate and returns the echoed value.
Future<Object?> echoPrimitivesAndCollections() {
  return _echo(<String, Object?>{
    'int': 7,
    'double': 1.5,
    'bool': true,
    'string': 'fixture',
    'list': [1, 2, 3],
    'set': {1, 2, 3},
  });
}

/// Sends a [SendPort] itself as message content; ports are sendable,
/// unlike the [ReceivePort] used in [attemptSendUnsendableValue].
Future<bool> echoSendPort() async {
  final probePort = ReceivePort();
  final echoed = await _echo(probePort.sendPort);
  probePort.close();
  return echoed is SendPort;
}

/// A deeply immutable value shared, rather than copied, across the
/// isolate boundary.
const List<String> immutableSharedConstant = ['alpha', 'beta', 'gamma'];

/// Sends the same `const` list across the isolate boundary twice and
/// reports whether both echoed copies are identical, which is how the
/// runtime shares immutable/canonicalized data between isolates.
Future<bool> echoImmutableConstantTwiceAndCompareIdentity() async {
  final firstEcho = await _echo(immutableSharedConstant);
  final secondEcho = await _echo(immutableSharedConstant);
  return identical(firstEcho, secondEcho);
}

/// Sends a self-referencing `Map`; cyclic sendable data is supported by
/// isolate message passing, which preserves the cycle within one
/// message.
Future<bool> echoCyclicMap() async {
  final cyclic = <String, Object?>{};
  cyclic['self'] = cyclic;
  final echoed = await _echo(cyclic) as Map<Object?, Object?>;
  return identical(echoed['self'], echoed);
}

/// Attempts to send a [ReceivePort], which is not a sendable value, and
/// reports the runtime failure.
Future<String> attemptSendUnsendableValue() async {
  final probePort = ReceivePort();
  try {
    await _echo(probePort);
    return 'no error';
  } catch (error) {
    return 'caught: ${error.runtimeType}';
  } finally {
    probePort.close();
  }
}

/// Transfers a chunk of typed data to another isolate via
/// [TransferableTypedData] and materializes it on the receiving side.
Future<int> transferTypedData() async {
  final source = Uint8List.fromList([10, 20, 30, 40]);
  final transferable = TransferableTypedData.fromList([source]);
  final echoed = await _echo(transferable) as TransferableTypedData;
  final materialized = echoed.materialize().asUint8List();
  return materialized.fold<int>(0, (sum, value) => sum + value);
}

/// Materializing a [TransferableTypedData] a second time fails at
/// runtime because the underlying buffer was already consumed by the
/// first call.
Future<String> materializeTransferableTwice() async {
  final source = Uint8List.fromList([1, 2, 3]);
  final transferable = TransferableTypedData.fromList([source]);
  transferable.materialize();
  try {
    transferable.materialize();
    return 'no error';
  } catch (error) {
    return 'caught: ${error.runtimeType}';
  }
}

Future<Object?> _echo(Object? message) async {
  final receivePort = ReceivePort();
  try {
    await Isolate.spawn(echoEntryPoint, [receivePort.sendPort, message]);
    return await receivePort.first;
  } finally {
    receivePort.close();
  }
}
