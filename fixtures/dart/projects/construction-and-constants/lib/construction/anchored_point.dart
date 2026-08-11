/// Initialization-order and super-call fixtures for [DART-CAN-OBJ-001]: an
/// explicit super call, an implicit super call, a super-parameter forwarding
/// constructor, and a recorded initialization order spanning an
/// initializer-list expression, a superclass body, and a subclass body.
library;

/// Shared order log observed by [describeAnchoredPoints].
final List<String> anchorInitializationLog = <String>[];

double _logged(String tag, double value) {
  anchorInitializationLog.add(tag);
  return value;
}

/// Root of the anchor hierarchy: a zero-argument-compatible unnamed
/// constructor, callable implicitly by a subclass that mentions no `super`.
class Anchor {
  Anchor([this.originLabel = 'origin']) {
    anchorInitializationLog.add('Anchor.body:$originLabel');
  }

  final String originLabel;
}

/// Explicit super call, plus an initializer-list expression that runs before
/// the superclass constructor completes.
class LoggingFrame extends Anchor {
  LoggingFrame(double scale)
    : scale = _logged('LoggingFrame.initializerList', scale),
      super('logged-frame') {
    anchorInitializationLog.add('LoggingFrame.body');
  }

  final double scale;
}

/// Implicit super call: no `super` appears, so the compiler inserts a
/// zero-argument call to [Anchor]'s unnamed constructor.
class ImplicitFrame extends Anchor {
  ImplicitFrame(this.label) {
    anchorInitializationLog.add('ImplicitFrame.body:$label');
  }

  final String label;
}

/// Super-parameter forwarding: `super.originLabel` both declares the
/// parameter and forwards it to the implicit trailing super call.
class SuperParamFrame extends Anchor {
  SuperParamFrame(super.originLabel, this.scale) {
    anchorInitializationLog.add('SuperParamFrame.body:$scale');
  }

  final double scale;
}

/// Runs each frame constructor once and reports the accumulated order log,
/// clearing it first so repeated calls stay independent.
List<String> describeAnchoredPoints() {
  anchorInitializationLog.clear();
  LoggingFrame(2);
  final List<String> loggingFrameOrder = List<String>.of(
    anchorInitializationLog,
  );

  anchorInitializationLog.clear();
  ImplicitFrame('implicit');
  final List<String> implicitFrameOrder = List<String>.of(
    anchorInitializationLog,
  );

  anchorInitializationLog.clear();
  final superParamFrame = SuperParamFrame('forwarded', 4);

  return <String>[
    'LoggingFrame order (initializer list before super body before own body): '
        '$loggingFrameOrder',
    'ImplicitFrame order (implicit super() runs before own body): '
        '$implicitFrameOrder',
    'SuperParamFrame originLabel forwarded via super parameter: '
        '${superParamFrame.originLabel}',
  ];
}
