namespace Fixture.Roslyn.Policy;

// CS-CAN-102: AnalysisLevel / AnalysisMode interaction.
// The project sets <AnalysisLevel>latest</AnalysisLevel> and
// <AnalysisMode>AllEnabledByDefault</AnalysisMode>. This file exists
// to surface the declared analysis level in coverage; the behavior
// difference between analysis levels (e.g., CA rules enabled at latest
// versus 8.0) is captured by the project-wide setting and the
// EnforceCodeStyleInBuild=true that carries .editorconfig severity
// into the build.
//
// Combined variants demonstrated together in the consumer build:
// - nullable enable (default) plus #nullable enable/disable per file
// - WarningLevel 4 plus AnalysisLevel latest
// - .editorconfig severity (RCAN001 = warning; promoted to error by build
//   configuration in the PolicyBoundary project)
// - globalconfig build_property (GeneratorProvenance / CatalogPrefix)
// - NoWarn CS0436 at project level
// - pragma disable/restore (PragmaSuppressed.cs)
// - SuppressMessageAttribute (SuppressMessageVariant.cs)
// - DiagnosticSuppressor (SuppressedEntry.cs)
public sealed class AnalysisLevelVariant
{
    public string Describe() => "AnalysisLevel=latest AnalysisMode=AllEnabledByDefault EnforceCodeStyleInBuild=true";
}
