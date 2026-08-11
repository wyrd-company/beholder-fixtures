/// Marks a class whose companion `.g.dart` part is produced by
/// `toolSummaryBuilder` (see `lib/src/builders.dart`).
///
/// The generated part shares the annotated declaration's library and its
/// private declarations, so generated members may reference private fields
/// and top-level functions declared alongside the annotated class.
class ToolSummary {
  const ToolSummary();
}

/// Marks a class whose generated description is emitted as its own
/// standalone library by `crateManifestBuilder`, distinct from a `part of`
/// output. The generated library has its own private scope, separate from
/// the annotated declaration's library.
class CrateManifest {
  const CrateManifest();
}
