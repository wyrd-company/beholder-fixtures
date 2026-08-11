namespace Catalog.Core;

public sealed record CatalogItem(int Id, string Name, decimal Price);

public sealed record CatalogCollection(string Owner, IReadOnlyList<CatalogItem> Items)
{
    public int Count => Items.Count;

    public CatalogItem? FindById(int id)
    {
        foreach (var item in Items)
        {
            if (item.Id == id)
            {
                return item;
            }
        }

        return null;
    }
}

public static class CatalogSamples
{
    public static CatalogCollection CreateSample()
    {
        return new CatalogCollection(
            "warehouse-alpha",
            new[]
            {
                new CatalogItem(1, "Canvas", 12.50m),
                new CatalogItem(2, "Ink", 8.20m),
                new CatalogItem(3, "Brush", 5.75m),
            });
    }
}
