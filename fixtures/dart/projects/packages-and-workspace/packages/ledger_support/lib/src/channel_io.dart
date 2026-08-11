import 'dart:io';

/// `dart:io`-backed channel description, selected by the conditional
/// export in `channel.dart` whenever `dart:io` is available (the `vm-jit`
/// and `native-aot` build contexts this project declares).
String describeChannel() {
  return 'io-channel(${Platform.operatingSystem}, pid=${pid})';
}
