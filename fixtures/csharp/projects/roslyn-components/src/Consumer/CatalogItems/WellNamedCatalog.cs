using Fixture.Roslyn.Generator;

namespace Fixture.Roslyn.Catalog;

// CS-CAN-016: correctly suffixed; satisfies the naming analyzer with no diagnostic.
// Contrasts with ShippingRecord (unsuppressed violation) and SuppressedEntry
// (suppressed violation).
[GenerateCatalog("WellNamed")]
public partial class WellNamedCatalog
{
    public string Label => CatalogName;
}
