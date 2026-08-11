/// Standalone entry-point script for `Isolate.spawnUri`. It is loaded by
/// its own file URI rather than imported as a library, so it declares
/// its own `main` rather than a named entry-point function.
library;

import 'dart:isolate';

void main(List<String> args, SendPort sendPort) {
  sendPort.send('spawnUri received args=$args');
}
