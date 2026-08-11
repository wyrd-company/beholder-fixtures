namespace GenericsAndDispatch.Core.Dispatch;

public static class ArgumentForms
{
    public static string Format(string title, int count = 1, bool upper = false)
    {
        string result = $"{title}:{count}";
        return upper ? result.ToUpperInvariant() : result;
    }

    public static int Sum(params int[] values) => values.Sum();

    public static int SumSpan(params ReadOnlySpan<int> values)
    {
        int total = 0;
        foreach (var v in values) total += v;
        return total;
    }

    public static int Collect(params IEnumerable<int> values) => values.Sum();

    public static string Join(string separator = ",", params string[] parts) => string.Join(separator, parts);

    public static void Run()
    {
        // Reordered named arguments and omitted optional defaults.
        string a1 = Format("widget");
        string a2 = Format(count: 5, title: "gadget");
        string a3 = Format("thing", upper: true);
        string a4 = Format(title: "mixed", count: 2, upper: false);

        // Duplicate/out-of-position names are invalid (not fixture); valid reordered form above.

        // Array params normal and expanded, including empty expansion.
        int s1 = Sum(1, 2, 3);
        int s2 = Sum([1, 2, 3]);
        int s3 = Sum([]);
        int s4 = Sum();

        // Span and enumerable params collections (C# 13).
        int span1 = SumSpan(1, 2, 3);
        int span2 = SumSpan([1, 2, 3]);
        Span<int> buffer = stackalloc int[3] { 1, 2, 3 };
        int span3 = SumSpan(buffer);
        int coll1 = Collect(1, 2, 3);
        int coll2 = Collect([1, 2, 3]);

        // Source evaluation order for optional params is left-to-right at call.
        int counter = 0;
        string eval = Format(Next(ref counter), NextInt(ref counter), upper: NextBool(ref counter));

        // Overload competition between array and span params.
        string j1 = Join(",", "a", "b");
        string j2 = Join(parts: ["a", "b"]);

        // Caller-baked default mismatch represented by metadata constant: default is 1.
        string defaultDemo = Format("demo");

        _ = a1; _ = a2; _ = a3; _ = a4;
        _ = s1; _ = s2; _ = s3; _ = s4;
        _ = span1; _ = span2; _ = span3; _ = coll1; _ = coll2;
        _ = eval; _ = j1; _ = j2; _ = defaultDemo;
    }

    private static string Next(ref int counter) => $"name-{counter++}";
    private static int NextInt(ref int counter) => counter++;
    private static bool NextBool(ref int counter) => (counter++ % 2) == 0;
}
