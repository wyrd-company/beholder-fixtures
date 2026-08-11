/// Observable implicit constructors, interfaces, and supertypes for DART-CAN-DIAG-008.
library;

// Implicit default constructor: no explicit constructor declared.
class ImplicitDefault {
  String describe() => 'implicit';
}

// Use of implicit default constructor across a library boundary is observed
// via the instantiation below.
ImplicitDefault makeImplicit() => ImplicitDefault();

// Implicit interface: each class implicitly defines an interface.
// `ImplementsImplicit` implements that interface without inheriting the class.
class ImplementsImplicit implements ImplicitDefault {
  @override
  String describe() => 'implements-implicit';
}

// Implicit supertype: every class implicitly extends `Object` when no super
// type is declared. Observed via inherited members like `toString` and
// `hashCode` from Object.
String objectSupertypeDemo(ImplicitDefault value) => value.toString();

// Observable implicit interfaces and supertypes are language-defined; their
// synthesized display names are not asserted, only their observable behavior.
