namespace Fixture.AttributesAndMetadata.Core.NonInvariant;

/// <summary>
/// CS-CAN-127: avoids requiring any particular optimization or scheduling
/// choice. Whether the two produced tasks' continuations run inline or are
/// scheduled, and whether the runtime shares generic code or avoids an
/// intermediate boxing allocation for the constrained value-type call, are
/// never asserted — only the resulting values are.
/// </summary>
public static class OptimizationSchedulingLatitude
{
    public static async Task<int> DescribeTaskSchedulingIndependence()
    {
        var first = ProduceAsync(1);
        var second = ProduceAsync(2);
        var results = await Task.WhenAll(first, second);
        return results.Sum();
    }

    private static async Task<int> ProduceAsync(int seed)
    {
        await Task.Yield();
        return seed * 10;
    }

    public static bool DescribeBoxingIndependence<T>(T value)
        where T : struct
    {
        object boxed = value;
        return boxed.Equals(value);
    }
}
