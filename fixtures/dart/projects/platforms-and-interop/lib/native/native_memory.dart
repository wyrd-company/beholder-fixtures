/// Native memory management through the documented system allocator,
/// matching DART-CAN-PLAT-007's allocator/finalizer requirement. `malloc`
/// and `free` are bound directly from `libc.so.6` rather than through a
/// third-party allocator package, honoring this project's no-third-party
/// dependency constraint.
library;

import 'dart:ffi';

@Native<Pointer<Void> Function(IntPtr)>(symbol: 'malloc')
external Pointer<Void> nativeMalloc(int size);

@Native<Void Function(Pointer<Void>)>(symbol: 'free')
external void nativeFree(Pointer<Void> ptr);

/// A [NativeFinalizer] bound directly to the native `free` symbol's
/// address, so memory attached to it is released automatically when the
/// owning Dart object becomes unreachable, without a manual `free` call.
final NativeFinalizer freeFinalizer = NativeFinalizer(
  Native.addressOf<NativeFunction<Void Function(Pointer<Void>)>>(nativeFree),
);

/// Owns a native allocation and attaches it to [freeFinalizer]. It
/// implements [Finalizable] rather than being a bare [Pointer], since only
/// a genuine object (not a value type) can be attached to a finalizer.
final class NativeBuffer implements Finalizable {
  NativeBuffer(int sizeBytes) : pointer = nativeMalloc(sizeBytes) {
    freeFinalizer.attach(this, pointer.cast(), detach: this);
  }

  final Pointer<Void> pointer;

  /// Frees [pointer] immediately and detaches the finalizer, so it does not
  /// free the pointer a second time once this object becomes unreachable.
  void releaseNow() {
    freeFinalizer.detach(this);
    nativeFree(pointer);
  }
}
