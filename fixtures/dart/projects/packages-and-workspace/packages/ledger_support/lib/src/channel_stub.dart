/// Fallback channel description used when `dart:io` is unavailable, selected
/// by the conditional export in `channel.dart`. This project declares only
/// the `dart:io`-capable `vm-jit` and `native-aot` build contexts, so this
/// branch is not exercised by required validation; it exists so the
/// conditional export names a valid target on every configuration.
String describeChannel() => 'stub-channel(no-io)';
