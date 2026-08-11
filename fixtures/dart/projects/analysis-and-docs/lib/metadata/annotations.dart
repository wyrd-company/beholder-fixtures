/// Custom const annotations for DART-CAN-DIAG-005.
library;

/// Tag for workshop categorization.
class WorkshopTag {
  const WorkshopTag(this.label);
  final String label;
}

/// Marker for audit requirements.
class Audited {
  const Audited();
}

/// Generic annotation exercising generic annotation support where available.
///
/// Usage: `@Labeled<CatalogItem>('example')`
class Labeled<T> {
  const Labeled(this.value);
  final String value;
}

/// Repeatable workshop note where repeated annotations are demonstrated.
class WorkshopNote {
  const WorkshopNote(this.message);
  final String message;
}

/// Built-in annotation alias for clarity.
const workshopTag = WorkshopTag('workshop');
