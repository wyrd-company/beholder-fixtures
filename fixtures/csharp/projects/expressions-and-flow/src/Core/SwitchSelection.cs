namespace ExpressionsFlow.Core;

public enum FlavorKind
{
    Mild,
    Medium,
    Bold,
}

public static class SwitchSelection
{
    // Switch statement over enum - note enum not closed: default arm handles unknown values.
    public static string DescribeEnum(FlavorKind kind)
    {
        switch (kind)
        {
            case FlavorKind.Mild:
                return "mild";
            case FlavorKind.Medium:
                return "medium";
            case FlavorKind.Bold:
                return "bold";
            default:
                return "unknown";
        }
    }

    // Switch expression over nullable value with null arm
    public static string DescribeNullable(int? value) => value switch
    {
        null => "none",
        0 => "zero",
        > 0 => "positive",
        < 0 => "negative",
    };

    // Switch expression over records/classes with guarded patterns and tuple
    public static string DescribeItem(CatalogItem item) => item switch
    {
        BookItem { Pages: > 500 } => "tome",
        BookItem { Pages: > 100 } b when b.Author.Length > 0 => $"book-by-{b.Author}",
        CrateItem { Weight: > 50 } => "heavy-crate",
        CrateItem c => $"crate-{c.Weight}",
        _ => "unknown-item",
    };

    public static string DescribeTuple((int X, int Y) point) => point switch
    {
        (0, 0) => "origin",
        (0, var y) => $"y-axis {y}",
        (var x, 0) => $"x-axis {x}",
        var (x, y) when x == y => "diagonal",
        _ => "other",
    };

    // Switch statement with null handling for reference
    public static string DescribeNullableItem(CatalogItem? item)
    {
        switch (item)
        {
            case null:
                return "null";
            case BookItem b:
                return $"book {b.Label}";
            case CrateItem c:
                return $"crate {c.Label}";
            default:
                return "other";
        }
    }

    // Evaluation-order-sensitive pattern: side-effecting property accessed once per match attempt
    public sealed class OrderProbe
    {
        private int _calls;
        public int Value => ++_calls;
    }

    public static string EvaluationOrder(OrderProbe probe) => probe.Value switch
    {
        1 => "first",
        2 => "second",
        _ => "other",
    };

    // Guard effects: guard further filters after pattern matches
    public static string Guarded(int value) => value switch
    {
        int n when n % 2 == 0 => "even",
        int n when n % 3 == 0 => "triple",
        _ => "other",
    };

    // Exhaustiveness: switch expression below is exhaustive due to discard arm.
    // Without discard it would produce CS8509 non-exhaustive warning and throw SwitchExpressionException at runtime
    // if an unmatched value is evaluated. Diagnostic example (not live):
    //   FlavorKind k = (FlavorKind)99;
    //   string s = k switch { FlavorKind.Mild => "mild", FlavorKind.Medium => "medium" }; // CS8509 non-exhaustive

    // Subsumption error is a diagnostic:
    //   int x = value switch { _ => 1, 0 => 2 }; // CS8514 subsumed arm is unreachable
}

public static class SwitchExpressionHelpers
{
    public static string JoinLabels(IEnumerable<CatalogItem> items) => string.Join(",", items.Select(i => i.Label));
}
