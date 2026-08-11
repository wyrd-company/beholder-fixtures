/// Contrasts five resolution strategies for call syntax that reads
/// alike: ordinary virtual dispatch (resolved by the runtime type),
/// static-member dispatch, constructor dispatch, extension-method
/// dispatch, and extension-type dispatch. The latter three are
/// resolved at compile time and never vary with the runtime type.
library;

class Shape {
  String kind() => 'shape';

  static String describe() => 'a generic shape';
}

class Circle extends Shape {
  @override
  String kind() => 'circle';
}

/// Ordinary virtual dispatch: `shape.kind()` resolves to the override
/// on the runtime type of [shape] even though [shape] is statically
/// typed [Shape].
String virtualDispatch(Shape shape) => shape.kind();

/// Static-member dispatch: [Shape.describe] is resolved by the
/// declared class name at compile time and never varies by runtime
/// type.
String staticDispatch() => Shape.describe();

/// Constructor dispatch: `Circle()` always runs exactly the [Circle]
/// constructor named in source, never a subtype's constructor.
Circle constructorDispatch() => Circle();

extension ShapeLabel on Shape {
  String label() => 'extension-shape:$runtimeType';
}

extension CircleLabel on Circle {
  String label() => 'extension-circle:$runtimeType';
}

/// Extension-method dispatch: which `label()` applies is chosen by the
/// receiver expression's *static* type, not its runtime type. Because
/// [shape] is statically typed [Shape], [ShapeLabel.label] is the only
/// applicable extension at this call site — [CircleLabel] requires a
/// statically-[Circle] receiver — even when the runtime type is
/// [Circle].
String extensionDispatch(Shape shape) => shape.label();

extension type ShapeView(Shape shape) {
  /// Resolved statically from the extension type's own declared
  /// members; [ShapeView] has no runtime representation of its own and
  /// simply forwards to the wrapped [Shape], whose `kind()` call is
  /// itself an ordinary virtual dispatch.
  String kind() => 'view:${shape.kind()}';
}

/// Extension-type dispatch: `ShapeView(shape).kind()` is resolved from
/// the declared extension type, not from any runtime type of the
/// underlying representation object.
String extensionTypeDispatch(Shape shape) => ShapeView(shape).kind();
