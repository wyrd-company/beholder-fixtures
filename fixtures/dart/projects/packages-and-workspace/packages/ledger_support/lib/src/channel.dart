/// Conditional import in a workspace member (DART-CAN-PKG-006): resolves to
/// the `dart:io`-backed implementation whenever `dart:io` is available, and
/// to the portable stub otherwise.
export 'channel_stub.dart' if (dart.library.io) 'channel_io.dart';
