using System.Text.Json.Serialization;
using Catalog.Web.Models;

namespace Catalog.Web.Serialization;

[JsonSerializable(typeof(CatalogEntry))]
[JsonSerializable(typeof(PhysicalCatalogEntry))]
[JsonSerializable(typeof(DigitalCatalogEntry))]
[JsonSerializable(typeof(CatalogEnvelope))]
[JsonSerializable(typeof(CatalogEntry[]))]
[JsonSerializable(typeof(List<CatalogEntry>))]
public partial class CatalogJsonContext : JsonSerializerContext
{
}
