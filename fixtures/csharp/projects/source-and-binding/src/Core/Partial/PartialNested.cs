namespace SourceBinding.Core.Partial;

public partial class CatalogItem
{
    public partial class NestedPayload
    {
        public string Note { get; set; } = string.Empty;
    }
}

public partial class CatalogItem
{
    public partial class NestedPayload
    {
        public int Tag { get; set; }
    }
}
