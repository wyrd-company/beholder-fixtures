using System.Runtime.CompilerServices;

namespace Fixture.AttributesAndMetadata.Core.Recognized;

/// <summary>
/// Declares caller-information parameters and one caller-argument-expression
/// parameter, each with an explicit-override overload alongside the
/// omitted-argument form.
/// </summary>
public static class CallerInfoShowcase
{
    public static string Capture(
        string message,
        [CallerMemberName] string memberName = "",
        [CallerFilePath] string filePath = "",
        [CallerLineNumber] int lineNumber = 0)
        => $"{memberName} @ {Path.GetFileName(filePath)}:{lineNumber} - {message}";

    public static string CaptureArgumentExpression(
        int value,
        [CallerArgumentExpression(nameof(value))] string? expression = null)
        => $"{expression}={value}";

    public static string CaptureExplicit(string message)
        => Capture(message, memberName: "explicit-member", filePath: "explicit/path.cs", lineNumber: 999);

#line 500 "virtual/mapped/path.cs"
    public static string CaptureLineMapped(string message) => Capture(message);
#line default
}

/// <summary>
/// Exercises <see cref="CallerInfoShowcase"/> at a direct call site, through
/// a wrapper (which rebinds caller info to the wrapper's own call, not the
/// original caller), with explicit overrides, and with an argument
/// expression captured by its exact source spelling.
/// </summary>
public static class CallerInfoUsage
{
    public static string DirectCall() => CallerInfoShowcase.Capture("direct");

    public static string WrappedCall() => WrappedCapture("wrapped");

    private static string WrappedCapture(string message) => CallerInfoShowcase.Capture(message);

    public static string ExplicitOverrideCall() => CallerInfoShowcase.CaptureExplicit("explicit");

    public static string LineMappedCall() => CallerInfoShowcase.CaptureLineMapped("line-mapped");

    public static string ArgumentExpressionCall(int quantity) => CallerInfoShowcase.CaptureArgumentExpression(quantity * 2);
}
