using System.Runtime.CompilerServices;

namespace Fixture.AttributesAndMetadata.Contexts.CSharp10;

/// <summary>Caller-argument-expression capture became valid at its C# 10 version floor; built here under <c>LangVersion 10.0</c>.</summary>
public static class CallerArgumentExpressionBoundary
{
    public static string Capture(int value, [CallerArgumentExpression(nameof(value))] string? expression = null)
        => $"{expression}={value}";

    public static string Describe(int seed) => Capture(seed + 1);
}
