library;

extension VisibleGreeter on int {
  String greet() => 'visible';
}

extension HiddenGreeter on int {
  String greet() => 'hidden';
}
