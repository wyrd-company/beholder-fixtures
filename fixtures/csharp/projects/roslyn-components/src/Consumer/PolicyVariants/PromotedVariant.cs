using Fixture.Roslyn.Generator;

namespace Fixture.Roslyn.Policy;

// CS-CAN-102: warning promotion/demotion. The analyzer reports RCAN001 as
// warning by default; .editorconfig can promote it to error in StrictArea
// and the project-level WarningsNotAsErrors demotes it back, demonstrating
// promotion/demotion together with the StrictArea/RelaxedArea twins.
[GenerateCatalog("Promoted")]
public partial class PromotedVariant
{
    public string Note { get; set; } = string.Empty;
}
