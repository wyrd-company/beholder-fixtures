#define ATTR_META_SHOWCASE_ENABLED
using Fixture.AttributesAndMetadata.Core.Attributes;

namespace Fixture.AttributesAndMetadata.Core.Recognized;

/// <summary>
/// This file <c>#define</c>s <see cref="ConditionalSymbols.ShowcaseEnabled"/>
/// for itself alone (the project as a whole does not); every conditional
/// call and conditional attribute application written here is preserved.
/// </summary>
[ShowcaseDiagnostic]
public static class ConditionalCallSiteDefinedLocally
{
    public static void RecordFromDefinedFile()
        => ConditionalTrace.Trace(SideEffectCounter.Touch("defined-file"));
}
