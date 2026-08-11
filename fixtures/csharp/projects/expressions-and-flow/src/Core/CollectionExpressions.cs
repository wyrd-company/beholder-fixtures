using System.Collections.Immutable;
using System.Runtime.CompilerServices;

namespace ExpressionsFlow.Core;

[CollectionBuilder(typeof(CustomBuilder), nameof(CustomBuilder.Create))]
public sealed class CustomCollection : IEnumerable<int>
{
    private readonly List<int> _items;

    public CustomCollection(List<int> items) => _items = items;

    public IEnumerator<int> GetEnumerator() => _items.GetEnumerator();

    System.Collections.IEnumerator System.Collections.IEnumerable.GetEnumerator() => GetEnumerator();

    public int Count => _items.Count;
}

public static class CustomBuilder
{
    public static CustomCollection Create(ReadOnlySpan<int> items) => new(new List<int>(items.ToArray()));
}

public static class CollectionExpressions
{
    // Array target
    public static int[] ArrayExpression() => [1, 2, 3];

    public static int[] EmptyArray() => [];

    // Span target (shown locally without escaping)
    public static int SpanLength()
    {
        Span<int> span = [10, 20, 30];
        return span.Length;
    }

    public static int ReadOnlySpanLength()
    {
        ReadOnlySpan<int> span = [1, 2, 3, 4];
        return span.Length;
    }

    // Standard interfaces / collections
    public static List<int> ListExpression() => [1, 2, 3];

    public static HashSet<int> SetExpression() => [1, 2, 2, 3];

    public static Dictionary<string, int> DictionaryFromCollectionExpressionIsNotSupported()
    {
        // Dictionaries are not collection-expression targets; use initializer syntax instead.
        return new Dictionary<string, int> { ["a"] = 1 };
    }

    public static IEnumerable<int> InterfaceExpression() => [5, 6, 7];

    public static IReadOnlyList<int> ReadOnlyList() => [9, 8, 7];

    public static ImmutableArray<int> ImmutableArrayExpression() => [1, 2, 3];

    // Custom builder type
    public static CustomCollection BuilderExpression() => [1, 2, 3, 4];

    public static CustomCollection BuilderWithSpread(int[] extra) => [0, .. extra, 99];

    // Empty and spread forms with side effects
    private static int _spreadEval;

    private static IEnumerable<int> SideEffectSource()
    {
        _spreadEval++;
        yield return 10;
        _spreadEval++;
        yield return 20;
    }

    public static int[] SpreadWithSideEffects() => [1, .. SideEffectSource(), 3];

    public static int[] SpreadMultiple(int[] a, int[] b) => [.. a, .. b];

    // Evaluation order
    private static int NextValue()
    {
        _spreadEval++;
        return _spreadEval;
    }

    public static int[] EvaluationOrder() => [NextValue(), NextValue(), NextValue()];

    // No target type is diagnostic: var x = [1, 2, 3]; // CS9174 no target type
    // Count/capacity path:List/HashSet may use known count for capacity; demonstrated via list above.

    // Ref safety: collection expression over ref-struct span is valid only when not escaping.
    public static int SpanCount()
    {
        Span<int> span = [1, 2, 3, 4];
        return span.Length;
    }

    // Overload choice
    public static void AcceptArray(int[] values) => _ = values.Length;

    public static void AcceptSpan(ReadOnlySpan<int> span) => _ = span.Length;

    public static void OverloadChoice()
    {
        AcceptArray([1, 2, 3]);
        AcceptSpan([1, 2, 3]);
    }

    // Params interaction
    private static string Join(params int[] values) => string.Join(",", values);

    private static string JoinSpan(params ReadOnlySpan<int> span) => string.Join(",", span.ToArray());

    public static string ParamsWithCollectionExpression() => Join([1, 2, 3]);

    public static string ParamsSpanWithCollectionExpression() => JoinSpan([4, 5, 6]);

    // Selected concrete representation: IEnumerable<int> vs List<int> picks different runtime type
    public static Type ConcreteForInterface()
    {
        IEnumerable<int> seq = [1, 2, 3];
        return seq.GetType();
    }

    // Invalid builder attribute/method is a diagnostic:
    // [CollectionBuilder(typeof(BadBuilder), "Missing")] class Bad : IEnumerable<int> {} // CS9187

    public static int SpreadEvalCount => _spreadEval;
}
