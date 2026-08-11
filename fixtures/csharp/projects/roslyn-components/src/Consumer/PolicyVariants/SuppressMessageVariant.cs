using System.Diagnostics.CodeAnalysis;
using Fixture.Roslyn.Generator;

namespace Fixture.Roslyn.Policy;

// CS-CAN-102: SuppressMessage attribute. Suppresses RCAN001 via
// System.Diagnostics.CodeAnalysis.SuppressMessageAttribute, which has
// lower precedence than a DiagnosticSuppressor (RCSUP001) but higher than
// a global severity demotion.
[SuppressMessage("RoslynComponents.Naming", "RCAN001", Justification = "Fixture demonstrates SuppressMessageAttribute precedence.")]
[GenerateCatalog("MessageSuppressed")]
public partial class SuppressMessageVariant
{
    public string Tag { get; set; } = string.Empty;
}
