using Fixture.Roslyn.Generator;

namespace Fixture.Roslyn.Policy.RelaxedArea;

// CS-CAN-102: same source shape as StrictArea/PromotedViolation.cs, but under
// PolicyVariants/RelaxedArea where .editorconfig sets RCAN001 to silent.
// No diagnostic is emitted here, while the StrictArea twin is promoted.
[GenerateCatalog("Relaxed")]
public partial class SilentViolation
{
    public string Tag { get; set; } = string.Empty;
}
