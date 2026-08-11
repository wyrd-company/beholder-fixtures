/// Splits a PascalCase identifier into its lowercase word parts, e.g.
/// `TorqueWrench` -> `['torque', 'wrench']`. Used by `ToolSummaryGenerator`
/// and `CrateManifestGenerator` to derive the short, class-name-based
/// constant lists that demonstrate DART-CAN-BUILD-004's formatter-style
/// contrast.
List<String> splitPascalCase(String identifier) => identifier
    .replaceAllMapped(RegExp('(?<=[a-z0-9])(?=[A-Z])'), (match) => ' ')
    .split(' ')
    .map((word) => word.toLowerCase())
    .toList();
