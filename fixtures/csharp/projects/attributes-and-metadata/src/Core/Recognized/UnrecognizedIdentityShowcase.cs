namespace Fixture.AttributesAndMetadata.Core.Recognized.UnrecognizedIdentity;

/// <summary>
/// Shares its simple name with <see cref="System.Diagnostics.ConditionalAttribute"/>
/// but lives in a project-local namespace rather than <c>System.Diagnostics</c>.
/// Compiler-recognized attribute protocols match by full, namespace-qualified
/// identity, never by simple name alone, so this is an ordinary attribute
/// with no elision effect whatsoever — declared in its own namespace,
/// isolated from every file that imports the real
/// <c>System.Diagnostics.ConditionalAttribute</c>, so the two never collide.
/// </summary>
[AttributeUsage(AttributeTargets.Method)]
public sealed class ConditionalAttribute : Attribute
{
    public ConditionalAttribute(string symbol)
    {
        Symbol = symbol;
    }

    public string Symbol { get; }
}

public static class UnrecognizedIdentityShowcase
{
    private static int _callCount;

    public static int CallCount => _callCount;

    [ConditionalAttribute("NEVER_DEFINED_ANYWHERE_IN_THIS_PROJECT")]
    public static void AlwaysCalled() => _callCount++;
}

public static class UnrecognizedIdentityUsage
{
    /// <summary>
    /// Unlike a genuine <c>[Conditional]</c> call (see <c>ConditionalCalls.cs</c>),
    /// this call is never elided: the compiler only recognizes
    /// <see cref="System.Diagnostics.ConditionalAttribute"/> by its full
    /// namespace-qualified identity, so this same-named, differently-namespaced
    /// attribute has no special compiler behavior at all.
    /// </summary>
    public static string RecordUnconditionally()
    {
        UnrecognizedIdentityShowcase.AlwaysCalled();
        return $"unrecognized-identity-call-count={UnrecognizedIdentityShowcase.CallCount}";
    }
}
