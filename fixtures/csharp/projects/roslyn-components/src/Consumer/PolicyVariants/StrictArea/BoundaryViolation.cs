using Fixture.Roslyn.Generator;

namespace Fixture.Roslyn.Policy.StrictArea;

// CS-CAN-102: same source as RelaxedArea/BoundaryViolation.cs (identical class
// shape, attribute, and body). StrictArea .editorconfig promotes RCAN001 to
// error so this instance fails the build, while the RelaxedArea twin is
// suppressed to none and passes. Demonstrates same-source pass/fail by
// diagnostic policy.
[GenerateCatalog("Boundary")]
public partial class BoundaryViolation
{
    public string Tag { get; set; } = string.Empty;
}
