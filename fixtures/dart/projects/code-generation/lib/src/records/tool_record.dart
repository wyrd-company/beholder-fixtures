import '../annotations.dart';

part 'tool_record.g.dart';

/// Formats a display label. Private and top-level, so it is reachable only
/// from within this library and its parts — `tool_record.g.dart`'s generated
/// extension calls it directly (DART-CAN-BUILD-001's shared-private-name
/// relationship).
String _normalizeLabel(String label) => label.trim().toUpperCase();

/// A pinned, annotation-triggered builder (`toolSummaryBuilder`, registered
/// in `build.yaml`) emits `tool_record.g.dart`, the committed `part` output
/// for this class.
@ToolSummary()
class TorqueWrench {
  const TorqueWrench(this.label, this._calibrationNewtonMeters);

  final String label;

  /// Private, so only this library (including its parts) can read it. The
  /// generated part reads it directly, proving the part shares this
  /// library's private namespace.
  final double _calibrationNewtonMeters;

  double get calibrationNewtonMeters => _calibrationNewtonMeters;
}
