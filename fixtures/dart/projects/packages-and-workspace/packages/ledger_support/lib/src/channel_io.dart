import 'dart:ffi';
import 'dart:io';

/// `dart:io`-backed channel description, selected by the conditional
/// import in `channel.dart` whenever `dart:io` is available (the `vm-jit`
/// and `native-aot` build contexts this project declares). `Abi.current()`
/// names the operating-system-and-architecture target (for example
/// `linux_x64`) the compiled `native-aot` artifact ran under
/// (DART-CAN-PKG-008), alongside `Platform.operatingSystem`.
String describeChannel() {
  return 'io-channel(${Platform.operatingSystem}, ${Abi.current()}, pid=${pid})';
}
