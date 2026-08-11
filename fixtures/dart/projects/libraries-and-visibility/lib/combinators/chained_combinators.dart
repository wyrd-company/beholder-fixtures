library;

// Chained combinators apply left to right against the previous result:
// `show alpha, alpha, beta` (repeating `alpha`, which is harmless) narrows
// to {alpha, beta}, then `hide gamma` leaves {alpha, beta} unchanged since
// `gamma` was already excluded. `delta` never enters the namespace. The
// analyzer flags the repeated name and the multi-combinator chain as
// suspicious style; both are deliberate here to demonstrate the valid,
// language-defined chaining and repetition behavior.
// ignore: multiple_combinators, duplicate_shown_name
import 'multi_symbols.dart' show alpha, alpha, beta hide gamma;

String describeChainedCombinators() => '${alpha()}/${beta()}';
