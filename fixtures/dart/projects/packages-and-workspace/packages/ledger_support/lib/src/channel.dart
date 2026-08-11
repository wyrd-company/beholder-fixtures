/// Conditional import in a workspace member (DART-CAN-PKG-006): binds
/// `impl` to the `dart:io`-backed implementation whenever `dart:io` is
/// available, and to the portable stub otherwise, then forwards through it.
import 'channel_stub.dart' if (dart.library.io) 'channel_io.dart' as impl;

String describeChannel() => impl.describeChannel();
