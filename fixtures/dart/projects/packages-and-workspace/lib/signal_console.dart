/// Public façade for the `signal_console` package (DART-CAN-PKG-001,
/// DART-CAN-PKG-002): rooted at `lib/`, so importers use
/// `package:signal_console/signal_console.dart` regardless of this fixture's
/// directory name (`packages-and-workspace`). `lib/src/` remains reachable
/// through its own `package:` URI but is not re-exported here, unlike this
/// façade's `ConsoleApp` and `formatReport`.
library;

export 'src/console.dart' show ConsoleApp;
export 'src/formatting.dart' show formatReport;
