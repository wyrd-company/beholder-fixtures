library;

// Public `lib/src` separation: implementation lives under `src/`, and this
// façade re-exports only the selected public surface while importing an
// implementation-only dependency for its own convenience function below.
import 'src/internal_support.dart';

export 'src/public_gadgets.dart' show BaseGadget, ExtraGadget;

String describeLibrariesAndVisibility() => InternalHelper.helperLabel();
