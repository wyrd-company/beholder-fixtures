namespace GenericsAndDispatch.CSharp13;

public static class ParamsCollections
{
    public static int SumArray(params int[] values) => values.Sum();

    public static int SumSpan(params ReadOnlySpan<int> values)
    {
        int total = 0;
        foreach (var v in values) total += v;
        return total;
    }

    public static int CollectEnumerable(params IEnumerable<int> values) => values.Sum();

    // Builder shape for params collection with Create.
    public static int FromBuilder(params Span<int> values)
    {
        int total = 0;
        foreach (var v in values) total += v;
        return total;
    }

    public static void Run()
    {
        int a1 = SumArray(1, 2, 3);
        int a2 = SumArray([1, 2, 3]);
        int a3 = SumArray([]);

        int s1 = SumSpan(1, 2, 3);
        int s2 = SumSpan([1, 2, 3]);
        Span<int> buffer = stackalloc int[2] { 4, 5 };
        int s3 = SumSpan(buffer);
        int s4 = SumSpan();

        int e1 = CollectEnumerable(1, 2, 3);
        int e2 = CollectEnumerable([1, 2, 3]);

        // Array versus span overload selection prefers span when ReadOnlySpan target and span argument.
        int chooseSpan = SumSpan([1, 2, 3]);
        int chooseArray = SumArray([1, 2, 3]);

        _ = a1; _ = a2; _ = a3;
        _ = s1; _ = s2; _ = s3; _ = s4;
        _ = e1; _ = e2;
        _ = chooseSpan; _ = chooseArray;
    }
}
