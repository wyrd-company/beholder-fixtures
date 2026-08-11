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

    public InventoryInterpolatedStringHandler(int literalLength, int formattedCount, string label, out bool shouldAppend)
    {
        shouldAppend = label.Length > 0;
        _builder = new System.Text.StringBuilder(literalLength);
        _ = formattedCount;
        _builder.Append($"[{label}]");
    }

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

    public string ToStringAndClear() => _builder.ToString();

    public override string ToString() => _builder.ToString();
}

[InterpolatedStringHandler]
public ref struct ConditionalHandler
{
    private readonly System.Text.StringBuilder _builder;
    private readonly bool _shouldAppend;

    public ConditionalHandler(int literalLength, int formattedCount, bool condition, out bool shouldAppend)
    {
        shouldAppend = condition;
        _shouldAppend = shouldAppend;
        _builder = new System.Text.StringBuilder(literalLength);
        _ = formattedCount;
    }

    public void AppendLiteral(string s)
    {
        if (_shouldAppend)
        {
            _builder.Append(s);
        }
    }

    public void AppendFormatted<T>(T value)
    {
        if (_shouldAppend)
        {
            _builder.Append(value?.ToString());
        }
    }

    public string ToStringAndClear() => _builder.ToString();
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

    // Handler with forwarded receiver/arguments: compiler forwards label and controls construction via out shouldAppend
    public static string HandlerWithForwarded(string label, int count)
    {
        return FormatForwarded(label, $"catalog:{label}:{count}");
    }

    private static string FormatForwarded(string label, [InterpolatedStringHandlerArgument("label")] InventoryInterpolatedStringHandler handler)
    {
        return handler.ToStringAndClear();
    }

    // Conditional handler: holes are skipped when condition is false via out shouldAppend protocol
    private static int _holeEvals;

    private static int CountedHole()
    {
        _holeEvals++;
        return 99;
    }

    public static string ConditionalWithHandler(bool condition, int value)
    {
        return FormatConditional(condition, $"value:{value}");
    }

    public static int ConditionalHoleCount(bool condition)
    {
        _holeEvals = 0;
        FormatConditional(condition, $"value:{CountedHole()}");
        return _holeEvals;
    }

    private static string FormatConditional(bool condition, [InterpolatedStringHandlerArgument("condition")] ConditionalHandler handler)
    {
        return handler.ToStringAndClear();
    }

    // String versus handler overload set: same method name, different parameter type
    public static void Process(string text) => _ = text.Length;

    public static void Process(InventoryInterpolatedStringHandler handler) => _ = handler.ToStringAndClear();

    public static void OverloadChoice(string label)
    {
        // Handler overload is selected for interpolated string argument without cast
        Process($"label:{label}");
        // String overload is selected when explicitly cast to string
        Process((string)$"label:{label}");
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

    // Kept hole evaluation for non-handler path (always evaluates)
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
