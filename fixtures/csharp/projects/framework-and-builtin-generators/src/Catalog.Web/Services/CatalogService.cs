using Catalog.Web.Logging;
using Catalog.Web.Models;
using Microsoft.Extensions.Logging;

namespace Catalog.Web.Services;

public sealed class CatalogService
{
    private readonly ILogger<CatalogService> _logger;
    private readonly Dictionary<int, CatalogEntry> _entries = new();

    public CatalogService(ILogger<CatalogService> logger)
    {
        _logger = logger;
        _entries[1] = new PhysicalCatalogEntry(1, "Canvas", 0.5);
        _entries[2] = new DigitalCatalogEntry(2, "Ink Guide", "https://example.test/guide");
        _entries[3] = new PhysicalCatalogEntry(3, "Brush", 0.2);
    }

    public IReadOnlyList<CatalogEntry> ListAll() => _entries.Values.ToList();

    public CatalogEntry? FindById(int id)
    {
        if (_entries.TryGetValue(id, out var entry))
        {
            CatalogLogger.CatalogViewed(_logger, id.ToString(), "system");
            return entry;
        }

        CatalogLogger.EntryNotFound(_logger, id, "main");
        return null;
    }

    public CatalogEntry Create(CatalogEntry entry)
    {
        _entries[entry.Id] = entry;
        CatalogLogger.EntryCreated(_logger, entry.Id, entry.Name);
        return entry;
    }

    public CatalogEnvelope BuildEnvelope(string catalogId)
    {
        var entries = ListAll();
        CatalogLogger.SerializingCatalog(_logger, catalogId, entries.Count);
        return new CatalogEnvelope(catalogId, entries, DateTimeOffset.UtcNow);
    }
}
