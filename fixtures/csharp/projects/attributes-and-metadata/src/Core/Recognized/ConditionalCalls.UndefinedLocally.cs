using Fixture.AttributesAndMetadata.Core.Attributes;

namespace Fixture.AttributesAndMetadata.Core.Recognized;

/// <summary>
/// This file never defines <see cref="ConditionalSymbols.ShowcaseEnabled"/>,
/// and the project itself leaves it undefined by default; the conditional
/// call below (and its side-effecting argument) and the conditional
/// attribute application are both omitted from this file's compiled shape.
/// </summary>
[ShowcaseDiagnostic]
public static class ConditionalCallSiteUndefinedLocally
{
    public static void RecordFromUndefinedFile()
        => ConditionalTrace.Trace(SideEffectCounter.Touch("undefined-file"));
}
