library;

// A legal export cycle: `cycle_a` exports `cycle_b`, which exports
// `cycle_a` back. Export cycles, unlike some other directive cycles, are
// permitted.
export 'cycle_b.dart';
export '../src/public_gadgets.dart' show ExtraGadget;
