using System.Text.Json;
using Catalog.Web.Models;

namespace Catalog.Web.Serialization;

public static class CatalogJsonService
{
    public static string SerializeWithContext(CatalogEnvelope envelope)
    {
        return JsonSerializer.Serialize(envelope, CatalogJsonContext.Default.CatalogEnvelope);
    }

    public static string SerializeWithReflection(CatalogEnvelope envelope)
    {
        return JsonSerializer.Serialize(envelope);
    }

    public static string SerializePolymorphicWithContext(CatalogEntry entry)
    {
        return JsonSerializer.Serialize(entry, CatalogJsonContext.Default.CatalogEntry);
    }

    public static CatalogEnvelope? DeserializeWithContext(string json)
    {
        return JsonSerializer.Deserialize(json, CatalogJsonContext.Default.CatalogEnvelope);
    }

    public static CatalogEnvelope? DeserializeWithReflection(string json)
    {
        return JsonSerializer.Deserialize<CatalogEnvelope>(json);
    }

    public static JsonSerializerOptions CreateOptionsWithContext()
    {
        return new JsonSerializerOptions
        {
            TypeInfoResolver = CatalogJsonContext.Default,
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
            WriteIndented = false,
        };
    }
}
