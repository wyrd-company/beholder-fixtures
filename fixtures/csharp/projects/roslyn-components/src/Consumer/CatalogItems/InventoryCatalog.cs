using Fixture.Roslyn.Generator;

namespace Fixture.Roslyn.Catalog;

// CS-CAN-015: consumes generator pipeline (syntax + symbols + AdditionalFiles +
// analyzer config + metadata). The generator emits a partial counterpart that
// provides CatalogName, GeneratorProvenance, GeneratedHintName, and
// DescribeCatalog(), and reports diagnostic RCGEN001 with recorded provenance.
[GenerateCatalog("Inventory")]
public partial class InventoryCatalog
{
    public int ItemCount { get; set; }

    public string Summary() => $"{DescribeCatalog()} items={ItemCount}";
}
