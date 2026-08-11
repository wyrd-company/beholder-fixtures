namespace Catalog.Web.Generated;

public sealed partial class CheckedInCatalogView
{
    public string FormatTitle() => $"Catalog: {Title}";

    public int LabelCount => Labels.Count;

    public static CheckedInCatalogView CreateSample()
    {
        return new CheckedInCatalogView
        {
            Title = "Sample Catalog",
            Labels = new[] { "sample", "checked-in", "generated" },
        };
    }
}
