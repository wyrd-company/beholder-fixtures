using Microsoft.Extensions.Logging;

namespace Catalog.Web.Logging;

public static partial class CatalogLogger
{
    [LoggerMessage(EventId = 1001, Level = LogLevel.Information, Message = "Catalog {CatalogId} viewed by {User}")]
    public static partial void CatalogViewed(ILogger logger, string catalogId, string user);

    [LoggerMessage(EventId = 1002, Level = LogLevel.Warning, Message = "Catalog entry {EntryId} not found in {CatalogId}")]
    public static partial void EntryNotFound(ILogger logger, int entryId, string catalogId);

    [LoggerMessage(EventId = 1003, Level = LogLevel.Debug, Message = "Serializing catalog {CatalogId} with {EntryCount} entries")]
    public static partial void SerializingCatalog(ILogger logger, string catalogId, int entryCount);

    [LoggerMessage(EventId = 1004, Level = LogLevel.Information, Message = "Created entry {EntryId} ({EntryName})")]
    public static partial void EntryCreated(ILogger logger, int entryId, string entryName);
}
