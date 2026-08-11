using Fixture.Roslyn.Generator;

namespace Fixture.Roslyn.Policy;

// CS-CAN-102: pragma warning disable/restore. The pragma suppresses RCAN001
// for the enclosed region, demonstrating pragma precedence; the warning
// outside the pragma would still be reported.
#pragma warning disable RCAN001
[GenerateCatalog("PragmaSuppressed")]
public partial class PragmaSuppressed
{
    public string Value { get; set; } = string.Empty;
}
#pragma warning restore RCAN001
