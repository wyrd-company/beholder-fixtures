using System.Runtime.CompilerServices;

namespace ExpressionsFlow.CSharp10;

[InterpolatedStringHandler]
public ref struct CSharp10Handler
{
    private readonly System.Text.StringBuilder _builder;

    public CSharp10Handler(int literalLength, int formattedCount)
    {
        _builder = new System.Text.StringBuilder(literalLength);
        _ = formattedCount;
    }

    public void AppendLiteral(string value) => _builder.Append(value);

    public void AppendFormatted<T>(T value) => _builder.Append(value?.ToString());

    public string ToStringAndClear() => _builder.ToString();
}

public static class InterpolatedHandlers
{
    // Constant interpolated string (C# 10)
    private const string Prefix = "catalog";

    public const string ConstantText = $"{Prefix}:entry";

    public static string ToStringForm(string label, int count) => $"item:{label}={count}";

    public static FormattableString ToFormattable(string label, int count) => $"item:{label}={count}";

    public static string ViaHandler(string label, int count)
    {
        CSharp10Handler handler = new(20, 2);
        handler.AppendLiteral("catalog:");
        handler.AppendFormatted(label);
        handler.AppendLiteral(":");
        handler.AppendFormatted(count);
        return handler.ToStringAndClear();
    }

    public static void HandlerOverload(CSharp10Handler handler) => _ = handler.ToStringAndClear();

    public static void StringOverload(string value) => _ = value.Length;

    public static void OverloadSelection(string label)
    {
        StringOverload($"label:{label}");
        HandlerOverload($"label:{label}");
    }
}
