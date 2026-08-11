using System.Reflection;

namespace Fixture.AttributesAndMetadata.Core.Reflection;

/// <summary>
/// Locates the compiler-synthesized entry-point type produced by top-level
/// statements via <see cref="Assembly.EntryPoint"/>, never by matching its
/// synthesized type name, per CS-CAN-125. Intended to be called from within
/// an executable assembly built from top-level statements.
/// </summary>
public static class TopLevelTypeObservation
{
    public static string Describe()
    {
        var entryPoint = Assembly.GetEntryAssembly()?.EntryPoint;
        var declaringType = entryPoint?.DeclaringType;

        return declaringType is null
            ? "no-entry-point-found"
            : $"top-level-entry-type-present entry-method-static={entryPoint!.IsStatic}";
    }
}
