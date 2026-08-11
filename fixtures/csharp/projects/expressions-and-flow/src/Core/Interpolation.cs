using System.Globalization;
using System.Runtime.CompilerServices;

namespace ExpressionsFlow.Core;

[InterpolatedStringHandler]
public ref struct InventoryInterpolatedStringHandler
{
    private readonly System.Text.StringBuilder _builder;

    public InventoryInterpolatedStringHandler(int literalLength, int formattedCount)
    {
        _builder = new System.Text.StringBuilder(literalLength);
        _ = formattedCount;
    }

    // Overload with receiver/arguments forwarding could capture additional state;
    // this minimal handler demonstrates conditional Append and forwarded literal length.
    public void AppendLiteral(string s) => _builder.Append(s);

    public void AppendFormatted<T>(T value) => _builder.Append(value?.ToString());

    public void AppendFormatted<T>(T value, string? format) where T : IFormattable
    {
        _builder.Append(value?.ToString(format, CultureInfo.InvariantCulture));
    }

    public void AppendFormatted<T>(T value, int alignment)
    {
        string text = value?.ToString() ?? string.Empty;
        if (alignment != 0)
        {
            text = alignment > 0 ? text.PadLeft(alignment) : text.PadRight(-alignment);
        }

        _builder.Append(text);
    }

    public void AppendFormatted<T>(T value, int alignment, string format) where T : IFormattable
    {
        string text = value?.ToString(format, CultureInfo.InvariantCulture) ?? string.Empty;
        if (alignment != 0)
        {
            text = alignment > 0 ? text.PadLeft(alignment) : text.PadRight(-alignment);
        }

        _builder.Append(text);
    }

    public bool AppendIfAvailable(string label, int count)
    {
        if (count > 0)
        {
            _builder.Append(label);
            _builder.Append(':');
            _builder.Append(count);
            return true;
        }

        return false;
    }

    public string ToStringAndClear() => _builder.ToString();

    public override string ToString() => _builder.ToString();
}

public static class Interpolation
{
    // Identical interpolation converted to different targets
    public static string ToStringInterpolation(string label, int count) => $"stock:{label}={count}";

    public static FormattableString ToFormattableString(string label, int count) => $"stock:{label}={count}";

    // Constant string interpolation (C# 10)
    private const string Prefix = "catalog";

    public const string ConstantInterpolated = $"{Prefix}:item";

    // Raw and verbatim forms
    public static string RawInterpolation(string label) => $"""raw:{label}:end""";

    public static string VerbatimInterpolation(string label) => $@"verbatim:{label}:end";

    public static string RawMultiline(string label) =>
        $"""
        line1:{label}
        line2:{label}
        """;

    // Alignment and format
    public static string Aligned(string label, int count) => $"|{label,10}|{count:D4}|";

    public static string Formatted(double value) => $"{value:F2}";

    public static string CultureSpecific(double value) => FormattableString.Invariant($"{value:F1}");

    // Skipped hole evaluation: argument not evaluated when handler conditionally skips
    private static int _holeEvals;

    private static int CountedHole()
    {
        _holeEvals++;
        return 99;
    }

    public static string HandlerWithForwarded(string label, int count)
    {
        // Forwarded receiver/arguments would be a logger/span; here we show handler with literal length.
        // The handler's AppendIfAvailable demonstrates conditional append.
        InventoryInterpolatedStringHandler handler = new(10, 2);
        handler.AppendLiteral("catalog:");
        handler.AppendFormatted(label);
        handler.AppendIfAvailable("count", count);
        return handler.ToStringAndClear();
    }

    public static void HandlerOverload(InventoryInterpolatedStringHandler handler) => _ = handler.ToString();

    public static void StringOverload(string text) => _ = text.Length;

    // String versus handler overload choice
    public static void OverloadChoice(string label)
    {
        // Prefers string overload when passed as string interpolation without handler target
        StringOverload($"label:{label}");
        // Prefers handler overload when target is handler
        HandlerOverload($"label:{label}");
    }

    // Ref-struct lifetime: handler is ref struct and cannot be boxed or captured
    public static string HandlerLifetime(string label, int count)
    {
        InventoryInterpolatedStringHandler handler = new(20, 2);
        handler.AppendLiteral("inv:");
        handler.AppendFormatted(label);
        handler.AppendFormatted(count);
        return handler.ToStringAndClear();
    }

    // Skipped hole: evaluation count shows hole evaluated only when interpolated.
    public static int HoleEvaluationCount()
    {
        _holeEvals = 0;
        _ = $"value:{CountedHole()}";
        return _holeEvals;
    }

    // Malformed handler is a diagnostic:
    //   [InterpolatedStringHandler] class Bad { } // CS9180 missing required Append methods

    public static string VerbatimRawCombo(string label) => $"""verbatim-raw:{label,5:X}""";
}
