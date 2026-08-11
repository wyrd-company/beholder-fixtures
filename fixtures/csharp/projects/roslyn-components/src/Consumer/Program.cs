using Fixture.Roslyn.Catalog;

namespace Fixture.Roslyn;

public static class Program
{
    public static void Main()
    {
        var inventory = new InventoryCatalog { ItemCount = 3 };
        System.Console.WriteLine(inventory.Summary());
        System.Console.WriteLine($"Provenance: {inventory.GeneratorProvenance}");
    }
}
