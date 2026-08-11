// Local marker with the same fully-qualified name the generator matches via
// ForAttributeWithMetadataName("Fixture.Roslyn.Generator.GenerateCatalogAttribute").
// The generator project defines the same type; this local copy lets the consumer
// compile without a runtime reference to the generator assembly.

namespace Fixture.Roslyn.Generator;

[System.AttributeUsage(System.AttributeTargets.Class, Inherited = false, AllowMultiple = false)]
public sealed class GenerateCatalogAttribute : System.Attribute
{
    public GenerateCatalogAttribute(string catalogName)
    {
        CatalogName = catalogName;
    }

    public string CatalogName { get; }
}
