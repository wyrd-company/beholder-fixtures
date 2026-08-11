namespace Catalog.CSharp13;

public sealed partial class PartialIndexerHost
{
    private int _base;

    public partial int this[int index] { get; set; }

    public partial string Title { get; set; }
}
