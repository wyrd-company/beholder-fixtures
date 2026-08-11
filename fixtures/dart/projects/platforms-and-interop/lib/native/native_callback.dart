/// A native callback bound through `dart:ffi`, matching
/// DART-CAN-PLAT-007's callback and callback-thread requirement. `qsort`
/// (glibc's `libc.so.6`) invokes [_compareInt32] synchronously, on the same
/// OS thread that calls [sortInt32Buffer]: unlike an isolate message or a
/// `NativeCallable` listener port, a `Pointer.fromFunction` callback passed
/// to a synchronous native call never crosses threads or isolates — the
/// native code calls straight back into the same Dart isolate, on the same
/// thread, before the native call returns.
library;

import 'dart:ffi';

import 'native_memory.dart' show nativeFree, nativeMalloc;

typedef _CompareNative = Int32 Function(Pointer<Int32>, Pointer<Int32>);

int _compareInt32(Pointer<Int32> a, Pointer<Int32> b) => a.value - b.value;

@Native<
  Void Function(
    Pointer<Void>,
    IntPtr,
    IntPtr,
    Pointer<NativeFunction<_CompareNative>>,
  )
>(symbol: 'qsort')
external void _qsort(
  Pointer<Void> base,
  int memberCount,
  int memberSizeBytes,
  Pointer<NativeFunction<_CompareNative>> comparator,
);

/// Sorts [values] ascending using the native `qsort`, whose comparator
/// callback is the Dart function [_compareInt32], exposed as a native
/// function pointer via [Pointer.fromFunction].
List<int> sortInt32Buffer(List<int> values) {
  final buffer = nativeMalloc(values.length * sizeOf<Int32>()).cast<Int32>();
  for (var i = 0; i < values.length; i++) {
    buffer[i] = values[i];
  }
  final comparator = Pointer.fromFunction<_CompareNative>(_compareInt32, 0);
  _qsort(buffer.cast(), values.length, sizeOf<Int32>(), comparator);
  final sorted = [for (var i = 0; i < values.length; i++) buffer[i]];
  nativeFree(buffer.cast());
  return sorted;
}
