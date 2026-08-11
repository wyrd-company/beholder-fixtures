using System.CodeDom.Compiler;

namespace Fixture.Roslyn.Catalog;

// CS-CAN-016: generated-code treatment. This type carries [GeneratedCode],
// which the analyzer is configured to ignore via
// ConfigureGeneratedCodeAnalysis(GeneratedCodeAnalysisFlags.None).
// The .editorconfig also marks this path as generated_code = true.
[GeneratedCode("Fixture.Roslyn.Generator", "1.0.0")]
public class GeneratedLike
{
    public string Payload { get; set; } = string.Empty;
}
