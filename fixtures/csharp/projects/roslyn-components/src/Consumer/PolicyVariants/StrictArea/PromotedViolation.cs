using Fixture.Roslyn.Generator;

namespace Fixture.Roslyn.Policy.StrictArea;

// CS-CAN-102: same source shape as RelaxedArea/SilentViolation.cs, but under
// PolicyVariants/StrictArea where .editorconfig promotes RCAN001 to error
// (then WarningsNotAsErrors demotes to warning in the default build; without
// that demotion this type would be a build error). Demonstrates "same source
// passing or failing by configuration."
[GenerateCatalog("Strict")]
public partial class PromotedViolation
{
    public string Tag { get; set; } = string.Empty;
}
