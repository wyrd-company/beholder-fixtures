namespace SourceBinding.Core.Partial;

public partial record CatalogRecord(int Id, string Label);

public partial record CatalogRecord
{
    public string Formatted => $"{Id}:{Label}";
}
