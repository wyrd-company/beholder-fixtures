namespace Catalog.Web.Generated;

public static class CatalogViewConsumer
{
    public static string Describe(CheckedInCatalogView view)
    {
        view.Render();
        return view.FormatTitle();
    }

    public static CheckedInCatalogView BuildFromEntry(string title, params string[] labels)
    {
        return new CheckedInCatalogView
        {
            Title = title,
            Labels = labels,
        };
    }
}
