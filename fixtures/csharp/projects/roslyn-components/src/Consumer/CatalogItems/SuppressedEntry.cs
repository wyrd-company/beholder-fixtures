using Fixture.Roslyn.Analyzer;
using Fixture.Roslyn.Generator;

namespace Fixture.Roslyn.Catalog;

// CS-CAN-016 + CS-CAN-102: same analyzer condition as ShippingRecord, but
// suppressed via SuppressCatalogNamingAttribute. The CatalogNamingSuppressor
// (RCSUP001) reports a suppression that outranks the analyzer's warning
// severity, demonstrating suppression precedence.
[GenerateCatalog("Suppressed")]
[SuppressCatalogNaming]
public partial class SuppressedEntry
{
    public string Note { get; set; } = string.Empty;
}
