using System;

namespace SourceBinding.Core.Partial;

[CatalogTag("part2")]
public partial class CatalogItem : IDisposable, IEquatable<CatalogItem>
{
    private string _label = string.Empty;

    public partial string Label
    {
        get => _label;
        set => _label = value;
    }

    public void Dispose() { }

    public bool Equals(CatalogItem? other) => other is not null && Id == other.Id;

    public override int GetHashCode() => Id;

    // Nested type split across partial parts (see PartialNested).
}
