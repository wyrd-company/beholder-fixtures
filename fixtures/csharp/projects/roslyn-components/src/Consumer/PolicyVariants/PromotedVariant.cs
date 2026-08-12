using Fixture.Roslyn.Generator;

namespace Fixture.Roslyn.Policy;

// CS-CAN-102: warning promotion/demotion. The analyzer reports RCAN001 as
// warning by default; the project-level WarningsNotAsErrors keeps it a warning
// in this consumer build. The same-source promotion-to-error versus suppression
// contrast is demonstrated by build configuration in the PolicyBoundary project.
[GenerateCatalog("Promoted")]
public partial class PromotedVariant
{
    public string Note { get; set; } = string.Empty;
}
