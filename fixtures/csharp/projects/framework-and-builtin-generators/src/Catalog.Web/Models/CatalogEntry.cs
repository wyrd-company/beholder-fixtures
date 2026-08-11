using System.Text.Json.Serialization;

namespace Catalog.Web.Models;

[JsonPolymorphic(TypeDiscriminatorPropertyName = "$kind")]
[JsonDerivedType(typeof(PhysicalCatalogEntry), "physical")]
[JsonDerivedType(typeof(DigitalCatalogEntry), "digital")]
public abstract record CatalogEntry(int Id, string Name);

public sealed record PhysicalCatalogEntry(int Id, string Name, double WeightKg) : CatalogEntry(Id, Name);

public sealed record DigitalCatalogEntry(int Id, string Name, string DownloadUrl) : CatalogEntry(Id, Name);

public sealed record CatalogEnvelope(string CatalogId, IReadOnlyList<CatalogEntry> Entries, DateTimeOffset UpdatedAt);
