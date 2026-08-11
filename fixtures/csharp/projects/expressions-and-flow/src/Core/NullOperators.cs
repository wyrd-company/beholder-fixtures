namespace ExpressionsFlow.Core;

public sealed class Container
{
    public string? Label { get; set; }

    public List<string> Tags { get; } = new();

    public string Describe() => Label ?? "empty";
}

public static class ContainerExtensions
{
    public static string DescribeExtension(this Container container) =>
        $"ext:{container.Label ?? "empty"}";

    public static int TagCount(this Container container) => container.Tags.Count;
}

public static class NullOperators
{
    // ?? and ??= with short-circuit and side effects
    private static int _evalCount;

    public static string Coalesce(string? left, string fallback)
    {
        _evalCount++;
        return left ?? fallback;
    }

    public static string CoalesceAssign(string? holder, string fallback)
    {
        holder ??= fallback;
        return holder;
    }

    public static string CoalesceChain(string? a, string? b, string c) => a ?? b ?? c;

    public static string? ConditionalAccess(Container? container) => container?.Label;

    public static string? ConditionalElementAccess(Container? container, int index) =>
        container?.Tags?[index];

    public static string? ConditionalElementAccessSafe(Container? container, int index) =>
        container?.Tags?[index] ?? "none";

    // Chained versus parenthesized conditional access: parentheses terminate one chain and change subsequent access
#pragma warning disable CS8602
    public static int? ChainedConditional(Container? container) => container?.Label.Length;
#pragma warning restore CS8602

    public static int? ParenthesizedConditional(Container? container) => (container?.Label)?.Length;

    public static string? ChainedAccess(Container? container) => container?.Label?.ToUpperInvariant();

    public static string? ParenthesizedAccess(Container? container) => (container?.Label)?.ToUpperInvariant();

    // Extension and ref member interaction via conditional access on extension-like pattern:
    // For a generic receiver, ?. still short-circuits.
    public static int GenericReceiver<T>(T? maybe) where T : class
    {
        return maybe?.ToString()?.Length ?? 0;
    }

    // Side-effecting receivers/arguments: receiver evaluated once, short-circuited when null.
    private static Container? SideEffectReceiver()
    {
        _evalCount++;
        return null;
    }

    private static string SideEffectArgument()
    {
        _evalCount++;
        return "fallback";
    }

    public static string SideEffectCoalesce(string? input) => input ?? SideEffectArgument();

    public static string? SideEffectConditional() => SideEffectReceiver()?.Label;

    // Null-forgiving ! does not change runtime value
    public static string Forgiving(string? maybe)
    {
        string forgiven = maybe!;
        // forgiven == maybe at runtime; ! only suppresses nullable warning
        return forgiven ?? string.Empty;
    }

    // Throw expression
    public static string ThrowExpression(string? input) => input ?? throw new ArgumentNullException(nameof(input));

    public static int ThrowInCoalesce(int? maybe) => maybe ?? throw new InvalidOperationException("missing");

    // Nullable value access
    public static int NullableValue(int? maybe) => maybe.HasValue ? maybe.Value : -1;

    public static int NullableGetValueOrDefault(int? maybe) => maybe.GetValueOrDefault(-1);

    // Flow-state effect: after ?? throw or null check, flow knows non-null.
    public static int FlowState(string? input)
    {
        if (input is null)
        {
            throw new ArgumentNullException(nameof(input));
        }

        // input is known non-null here
        return input.Length;
    }

    // Extension interaction via conditional access
    public static int ConditionalAccessExtension(Container? container) =>
        container?.DescribeExtension()?.Length ?? 0;

    public static int ExtensionTagCount(Container? container) =>
        container?.TagCount() ?? -1;

    // ! preserves reference identity: object.ReferenceEquals after forgiving
    public static bool ForgivingIdentity(string? input)
    {
        var a = input;
        var b = input!;
        return ReferenceEquals(a, b);
    }

    public static int EvalCount => _evalCount;
}
