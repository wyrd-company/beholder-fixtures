using Fixture.Roslyn.Generator;

namespace Fixture.Roslyn.Policy.RelaxedArea;

// CS-CAN-102: same source as StrictArea/BoundaryViolation.cs (identical class
// shape, attribute, and body). RelaxedArea .editorconfig sets RCAN001 to
// none so this instance passes, while the StrictArea twin is promoted to
// error and fails. Demonstrates same-source pass/fail by diagnostic policy.
[GenerateCatalog("Boundary")]
public partial class BoundaryViolation
{
    public string Tag { get; set; } = string.Empty;
}
