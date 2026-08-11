using System.Diagnostics;
using Fixture.AttributesAndMetadata.Core.Attributes;

namespace Fixture.AttributesAndMetadata.Core.Recognized;

/// <summary>Records observable side effects so elided calls and elided arguments can be told apart from evaluated ones.</summary>
public static class SideEffectCounter
{
    private static int _count;

    public static int Count => _count;

    public static string Touch(string tag)
    {
        _count++;
        return tag;
    }
}

/// <summary>
/// A <c>[Conditional]</c>-guarded method: the compiler omits both the call
/// and the evaluation of its arguments at any call site whose syntactic
/// location does not have <see cref="ConditionalSymbols.ShowcaseEnabled"/>
/// defined.
/// </summary>
public static class ConditionalTrace
{
    private static readonly List<string> Log = new();

    public static IReadOnlyList<string> Entries => Log;

    [Conditional(ConditionalSymbols.ShowcaseEnabled)]
    public static void Trace(string message) => Log.Add(message);
}
