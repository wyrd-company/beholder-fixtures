using Fixture.Roslyn.Generator;

namespace Fixture.Roslyn.Catalog;

// CS-CAN-016: public type in a Catalog namespace that does NOT end with "Catalog".
// When marked with [GenerateCatalog], the catalog naming analyzer (RCAN001)
// flags it as a naming violation - inspected via semantic state (symbol name
// and containing namespace), without changing emitted program semantics.
[GenerateCatalog("Shipping")]
public partial class ShippingRecord
{
    public string Destination { get; set; } = string.Empty;
}
