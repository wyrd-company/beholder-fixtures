namespace GenericsAndDispatch.Core.Dispatch;

public static class ArgumentForms
{
    public static string Format(string title, int count = 1, bool upper = false)
    {
        string result = $"{title}:{count}";
        return upper ? result.ToUpperInvariant() : result;
    }

    public static int Sum(params int[] values) => values.Sum();

    public static int Sum(ReadOnlySpan<int> values)
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

        // Array params normal and expanded, including empty expansion.
        int s1 = Sum(1, 2, 3);
        int s2 = Sum((int[])[1, 2, 3]);
        int s3 = Sum(Array.Empty<int>());
        int s4 = Sum();
        int s5 = Sum((int[])[1, 2, 3]);
        int s6 = Sum((ReadOnlySpan<int>)[1, 2, 3]);

        // Overload competition: same name Sum chooses array vs span based on argument.
        Span<int> buffer = stackalloc int[3] { 1, 2, 3 };
        int spanFromBuffer = Sum(buffer);
        int arrayFromCollection = Sum((int[])[1, 2, 3]);

        // Enumerable params collections (C# 13).
        int coll1 = Collect(1, 2, 3);
        int coll2 = Collect([1, 2, 3]);

        // Source evaluation order for optional params is left-to-right at call.
        int counter = 0;
        string eval = Format(Next(ref counter), NextInt(ref counter), upper: NextBool(ref counter));

        // Overload competition between array and span params with same name.
        string j1 = Join(",", "a", "b");
        string j2 = Join(parts: ["a", "b"]);

        // Caller-baked default mismatch: default value 1 is baked at call site.
        // ProducerV1 has count=1, ProducerV2 has count=99 but call without explicit count still bakes 1.
        string defaultBaked = Format("demo");
        string explicitDefault = Format("demo", 1);
        string v1 = DefaultsV1.Format("x");
        string v2 = DefaultsV2.Format("x");
        bool mismatch = v1 != v2;

        _ = a1; _ = a2; _ = a3; _ = a4;
        _ = s1; _ = s2; _ = s3; _ = s4; _ = s5; _ = s6;
        _ = spanFromBuffer; _ = arrayFromCollection; _ = coll1; _ = coll2;
        _ = eval; _ = j1; _ = j2; _ = defaultBaked; _ = explicitDefault; _ = mismatch;
    }

    private static string Next(ref int counter) => $"name-{counter++}";
    private static int NextInt(ref int counter) => counter++;
    private static bool NextBool(ref int counter) => (counter++ % 2) == 0;
}

public static class DefaultsV1
{
    public static string Format(string title, int count = 1) => $"{title}:{count}";
}

public static class DefaultsV2
{
    public static string Format(string title, int count = 99) => $"{title}:{count}";
}
