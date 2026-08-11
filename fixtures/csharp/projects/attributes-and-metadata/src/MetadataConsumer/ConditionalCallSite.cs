using Fixture.AttributesAndMetadata.Core.Recognized;

namespace Fixture.AttributesAndMetadata.MetadataConsumer;

/// <summary>
/// Unlike <c>Core</c>, this project's own compilation defines
/// <c>ATTR_META_SHOWCASE_ENABLED</c> (see <c>MetadataConsumer.csproj</c>).
/// <see cref="ConditionalTrace.Trace"/> is consumed here purely via metadata
/// (a compiled reference to <c>Core</c>), yet elision is still decided by
/// this call site's own compile-time symbols, not by how <c>Core</c> itself
/// was compiled — so the call and its side-effecting argument are preserved
/// here even though the equivalent call inside <c>Core</c>'s own undefined
/// files is elided.
/// </summary>
public static class ConditionalCallSiteFromMetadata
{
    public static void RecordFromMetadataConsumer()
        => ConditionalTrace.Trace(SideEffectCounter.Touch("metadata-consumer"));
}
