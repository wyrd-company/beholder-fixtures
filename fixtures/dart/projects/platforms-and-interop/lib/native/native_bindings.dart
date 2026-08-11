/// FFI bindings to documented system-library symbols, matching
/// DART-CAN-PLAT-007 and DART-CAN-FN-005. No native source is compiled by
/// this project: every symbol here already exists in glibc's `libc.so.6`
/// or `libm.so.6` on the pinned `linux_x64` target, and is bound either
/// through `@Native` (resolved from the process's already-loaded symbols)
/// or through an explicit [DynamicLibrary.open] lookup.
library;

import 'dart:ffi';

/// Mirrors POSIX `struct timespec` (`<time.h>`): two 64-bit signed
/// integers, matching the glibc x86-64 ABI layout. Its `external` fields
/// are FN-005's struct/union binding-context representative.
final class Timespec extends Struct {
  @Int64()
  external int tvSec;

  @Int64()
  external int tvNsec;
}

/// The `CLOCK_REALTIME` clock ID from glibc's `<time.h>`.
const int clockRealtime = 0;

/// `int clock_gettime(clockid_t, struct timespec *)`, declared by POSIX and
/// implemented by glibc's `libc.so.6`. `@Native` resolves `clock_gettime`
/// from the Dart process's already-loaded symbols (`libc.so.6` is always
/// loaded), so no [DynamicLibrary.open] call is needed for this symbol.
/// This is FN-005's `@Native`-bound external function: its native signature
/// (`Int32 Function(Int32, Pointer<Timespec>)`) is declared separately from
/// its Dart signature (`int Function(int, Pointer<Timespec>)`).
@Native<Int32 Function(Int32, Pointer<Timespec>)>(symbol: 'clock_gettime')
external int clockGettime(int clockId, Pointer<Timespec> timespec);

/// Reads the current wall-clock time through [clockGettime], demonstrating
/// a struct passed by pointer across the FFI boundary.
int currentWallClockSeconds(Pointer<Timespec> scratch) {
  final result = clockGettime(clockRealtime, scratch);
  if (result != 0) {
    throw StateError('clock_gettime failed with status $result');
  }
  return scratch.ref.tvSec;
}

/// A union view over four bytes: as one 32-bit word, or as four
/// individually addressable bytes. Demonstrates the struct-or-union
/// requirement's union side; the byte order visible through [asBytes] is a
/// non-portable observation (see
/// `diagnostics/non_portable_observations.dart`), never asserted here.
final class WordView extends Union {
  @Uint32()
  external int asWord;

  @Array(4)
  external Array<Uint8> asBytes;
}

/// `double sqrt(double)` from glibc's `libm.so.6`, resolved through an
/// explicit [DynamicLibrary.open] lookup rather than `@Native`, showing
/// FN-005's second supported binding mechanism. Marked `isLeaf: true`
/// because it allocates nothing, calls back into no Dart code, and never
/// blocks, so the VM can skip its usual native-call thread-state
/// transition — the "leaf call" DART-CAN-PLAT-007 requires.
final DynamicLibrary _libm = DynamicLibrary.open('libm.so.6');

final double Function(double) nativeSqrt = _libm
    .lookupFunction<Double Function(Double), double Function(double)>(
      'sqrt',
      isLeaf: true,
    );
