namespace Catalog.CSharp13;

public sealed partial class PartialIndexerHost
{
    public partial int this[int index]
    {
        get => _base + index;
        set => _base = value - index;
    }

    public partial string Title
    {
        get => $"title-{_base}";
        set => _base = value.Length;
    }
}
