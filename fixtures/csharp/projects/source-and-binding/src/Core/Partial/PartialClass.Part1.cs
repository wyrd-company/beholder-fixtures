using System;

namespace SourceBinding.Core.Partial;

[AttributeUsage(AttributeTargets.Class, AllowMultiple = true)]
public sealed class CatalogTagAttribute : Attribute
{
    public CatalogTagAttribute(string tag) => Tag = tag;
    public string Tag { get; }
}

[CatalogTag("part1")]
public partial class CatalogItem : IComparable<CatalogItem>
{
    public int Id { get; set; }

    public partial string Label { get; set; }

    public int CompareTo(CatalogItem? other) => Id.CompareTo(other?.Id ?? 0);
}
