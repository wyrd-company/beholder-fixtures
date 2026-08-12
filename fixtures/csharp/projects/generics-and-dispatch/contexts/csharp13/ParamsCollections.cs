namespace GenericsAndDispatch.CSharp13;

public static class ParamsCollections
{
    public static int Sum(params int[] values) => values.Sum();

    public static int Sum(ReadOnlySpan<int> values)
    {
        int total = 0;
        foreach (var v in values) total += v;
        return total;
    }

    public static int CollectEnumerable(params IEnumerable<int> values) => values.Sum();

    public static int SumBuilder(params Span<int> values)
    {
        int total = 0;
        foreach (var v in values) total += v;
        return total;
    }

    public static void Run()
    {
        int a1 = Sum(1, 2, 3);
        int a2 = Sum((int[])[1, 2, 3]);
        int a3 = Sum(Array.Empty<int>());
        int a4 = Sum();

        Span<int> buffer = stackalloc int[2] { 4, 5 };
        int s1 = Sum(buffer);
        int s2 = Sum((ReadOnlySpan<int>)[4, 5]);

        int e1 = CollectEnumerable(1, 2, 3);
        int e2 = CollectEnumerable([1, 2, 3]);

        // Array versus span overload selection.
        int chooseSpan = Sum((ReadOnlySpan<int>)[1, 2, 3]);
        int chooseArray = Sum((int[])[1, 2, 3]);

        int b1 = SumBuilder(1, 2, 3);

        _ = a1; _ = a2; _ = a3; _ = a4;
        _ = s1; _ = s2;
        _ = e1; _ = e2;
        _ = chooseSpan; _ = chooseArray; _ = b1;
    }
}
