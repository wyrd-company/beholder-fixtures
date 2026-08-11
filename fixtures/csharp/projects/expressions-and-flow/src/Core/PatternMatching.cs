namespace ExpressionsFlow.Core;

public abstract record CatalogItem(string Label);

public sealed record BookItem(string Label, int Pages, string Author) : CatalogItem(Label);

public sealed record CrateItem(string Label, int Weight) : CatalogItem(Label);

public sealed record PointItem(int X, int Y);

public sealed class SideEffectItem
{
    private string _label;
    private int _reads;

    public SideEffectItem(string label) => _label = label;

    public string Label
    {
        get
        {
            _reads++;
            return _label;
        }

        set => _label = value;
    }

    public int Reads => _reads;
}

public static class PatternMatching
{
    // Declaration pattern
    public static bool IsString(object value) => value is string s && s.Length > 0;

    // Type pattern with generic and discard
    public static bool IsBook(CatalogItem item) => item is BookItem;

    public static bool IsAnyBook(CatalogItem item) => item is var _;

    // Constant pattern
    public static bool IsZero(int value) => value is 0;

    public static bool IsLabelConstant(CatalogItem item) => item is { Label: "stock" };

    // Relational pattern
    public static string ClassifyWeight(int weight) => weight switch
    {
        < 0 => "negative",
        0 => "zero",
        > 0 and <= 10 => "light",
        > 10 and <= 100 => "medium",
        > 100 => "heavy",
    };

    // Logical pattern (and / or / not)
    public static bool IsBalanced(int value) => value is > 0 and < 100;

    public static bool IsSmallOrLarge(int value) => value is < 10 or > 90;

    public static bool IsNotNull(object? value) => value is not null;

    // Property pattern
    public static bool IsLargeBook(CatalogItem item) => item is BookItem { Pages: > 300, Author.Length: > 3 };

    // Side-effecting property pattern
    public static bool IsSideEffectMatch(SideEffectItem item) => item is { Label: "stock" };

    public static bool IsSideEffectLength(SideEffectItem item) => item is { Label.Length: > 3 };

    // Positional pattern via Deconstruct
    public static bool IsOrigin(PointItem point) => point is (0, 0);

    // Custom Deconstruct binding: TaggedPoint positional pattern
    public static bool IsTaggedOrigin(TaggedPoint point) => point is (0, 0);

    public static string DescribeTagged(TaggedPoint point) => point switch
    {
        (0, 0) => "origin",
        (1, var y) => $"x1 y{y}",
        _ => "other",
    };

    // Recursive pattern (nested property + positional)
    public static bool IsAuthoredBook(CatalogItem item) => item is BookItem { Author: var author, Pages: > 100 } && author.StartsWith("A");

    // List pattern
    public static bool IsSingleElementList<T>(IList<T> list) => list is [var single];

    public static bool IsFirstTwo(int[] values) => values is [1, 2, ..];

    // Slice pattern via list pattern with slice
    public static bool HasMiddleSlice(int[] values) => values is [_, .. var middle, _] && middle.Length > 0;

    // Var pattern
    public static bool IsVarCaptured(object input) => input is var captured && captured is not null;

    // Discard pattern
    public static bool IsDiscard(object input) => input is var _;

    // Null pattern
    public static bool IsNullPattern(object? input) => input is null;

    public static bool IsNonNullPattern(object? input) => input is not null;

    // Span-string constant pattern
    public static bool IsSpanConstant(ReadOnlySpan<char> span) => span is "stock";

    public static bool IsSpanHello(Span<char> span) => span is "hello";

    public static string ClassifySpan(ReadOnlySpan<char> span) => span switch
    {
        "hello" => "greeting",
        "stock" => "inventory",
        _ => "other",
    };

    // Guard (when) and side-effecting property evaluation via guard plus property pattern
    private static int _guardEvaluations;

    public static string GuardedBook(CatalogItem item) => item switch
    {
        BookItem b when TrackGuard(b) && b.Pages > 500 => "epic",
        BookItem b => $"book:{b.Pages}",
        CrateItem c => $"crate:{c.Weight}",
        _ => "other",
    };

    private static bool TrackGuard(BookItem item)
    {
        _guardEvaluations++;
        return true;
    }

    // Nullable narrowing
    public static int NullableNarrowing(int? value) => value is int v ? v : -1;

    // Span length via string pattern (kept) plus new span constant pattern above
    public static bool IsSpanLength(string? text) => text is string { Length: > 0 };

    // And/or variable restrictions: a variable declared inside an 'or' branch is not definite outside.
    // Valid form declares outside or uses var pattern to capture.
    public static int AndOrVariableRestriction(object input) => input switch
    {
        string s => s.Length,
        int n => n,
        _ => 0,
    };

    // Subsumed arms and invalid shape are diagnostics, shown as comments:
    //   switch (value) { case 1: ...; case 1: ...; } // CS8514 subsumed
    //   if (value is string { Nonexistent: 1 }) // CS0117 no such property for pattern shape
}

public static class PatternDeconstructHost
{
    // Instance Deconstruct for positional pattern
}

public sealed record TaggedPoint(int X, int Y)
{
    public void Deconstruct(out int x, out int y)
    {
        x = X;
        y = Y;
    }
}

public static class PointExtensions
{
    // Extension GetEnumerator not needed; extension Deconstruct could be defined but positional
    // already covered via instance Deconstruct above; list shape is covered via IList<T> pattern.
}
