namespace Fixture.Roslyn.Generator;

/// <summary>
/// Marker that requests the catalog generator to emit a partial counterpart.
/// The attribute itself is emitted by the generator's consumer infrastructure;
/// the generator matches by metadata name rather than by sharing this type.
/// </summary>
[System.AttributeUsage(System.AttributeTargets.Class, Inherited = false, AllowMultiple = false)]
public sealed class GenerateCatalogAttribute : System.Attribute
{
    public GenerateCatalogAttribute(string catalogName)
    {
        CatalogName = catalogName;
    }

    public string CatalogName { get; }
}
