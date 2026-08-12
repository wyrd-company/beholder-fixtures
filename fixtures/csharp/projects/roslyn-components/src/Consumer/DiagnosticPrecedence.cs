namespace Fixture.Roslyn;

// CS-CAN-102: diagnostic precedence surface. In order of increasing
// suppression power for analyzer diagnostics (RCAN001):
//   1. .editorconfig severity (per-path or global) - weakest
//   2. GlobalAnalyzerConfig.globalconfig severity
//   3. Project <NoWarn> / <WarningsNotAsErrors>
//   4. SuppressMessageAttribute (SuppressMessageVariant.cs)
//   5. #pragma warning disable (PragmaSuppressed.cs)
//   6. DiagnosticSuppressor (CatalogNamingSuppressor, SuppressedEntry.cs) - strongest
//
// Compiler errors (e.g., CS0246) are not downgradable through any of
// these; this fixture does not emit such errors, so the boundary is
// documented rather than demonstrated as invalid source.
public static class DiagnosticPrecedence
{
    // Same-source pass/fail is demonstrated by configuration in the dedicated
    // PolicyBoundary project: the Strict configuration promotes RCAN001 to an
    // error, the Relaxed configuration suppresses it.
    public const string StrictConfiguration = "PolicyBoundary (Strict)";
    public const string RelaxedConfiguration = "PolicyBoundary (Relaxed)";
    public const string AnalyzerId = "RCAN001";
    public const string SuppressorId = "RCSUP001";
    public const string GeneratorDiagnosticId = "RCGEN001";
}
