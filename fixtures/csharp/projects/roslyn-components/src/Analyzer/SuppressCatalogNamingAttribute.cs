namespace Fixture.Roslyn.Analyzer;

/// <summary>
/// Requests suppression of <c>RCAN001</c> for the annotated type.
/// The suppressor <see cref="CatalogNamingSuppressor"/> honors this marker.
/// Domain-neutral: the name carries no fixture-evaluation domain.
/// </summary>
[System.AttributeUsage(System.AttributeTargets.Class | System.AttributeTargets.Struct, Inherited = false, AllowMultiple = false)]
public sealed class SuppressCatalogNamingAttribute : System.Attribute
{
}
