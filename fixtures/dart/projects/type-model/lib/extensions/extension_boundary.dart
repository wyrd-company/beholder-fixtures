/// A second library for [DART-CAN-TYPE-005]'s prefixed explicit-application
/// and import-visibility variants: `extension_methods.dart` imports this
/// library with a prefix and applies [BoundaryOps] explicitly through it.
library;

extension BoundaryOps on int {
  int quadrupled() => this * 4;
}
