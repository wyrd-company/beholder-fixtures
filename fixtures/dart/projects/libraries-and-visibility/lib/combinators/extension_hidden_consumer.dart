library;

// Hiding `HiddenGreeter` removes it from extension-method resolution, so
// `greet()` below unambiguously resolves to `VisibleGreeter`.
import 'extension_hidden_source.dart' hide HiddenGreeter;

String describeHiddenExtensionConsumer() => 5.greet();
