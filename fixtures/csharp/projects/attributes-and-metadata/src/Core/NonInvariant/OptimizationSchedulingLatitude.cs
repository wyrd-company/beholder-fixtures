using System.Runtime.CompilerServices;

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

    public static bool DescribeDelegateCachingLatitude()
    {
        // Non-capturing lambdas are candidates for compiler-cached delegate
        // instances, but caching is never required; only the produced
        // results are compared, never delegate reference identity.
        Func<int, int> first = x => x + 1;
        Func<int, int> second = x => x + 1;
        return first(1) == second(1);
    }

    public static int DescribeStackHeapLoweringLatitude()
    {
        // Whether the runtime physically places this buffer on the stack or
        // promotes it elsewhere is never asserted; only the resulting value.
        Span<int> span = stackalloc int[4];
        for (var i = 0; i < span.Length; i++)
        {
            span[i] = i;
        }

        return span[^1];
    }

    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    private static int Increment(int value) => value + 1;

    public static int DescribeInliningLatitude(int seed)
        // Whether the JIT actually inlines this call is never asserted.
        => Increment(seed);

    public static int DescribeTailCallLatitude(int value, int accumulator = 0)
    {
        if (value <= 0)
        {
            return accumulator;
        }

        // Written in tail position; whether the JIT performs an actual tail
        // call is never asserted.
        return DescribeTailCallLatitude(value - 1, accumulator + value);
    }

    public static async Task<int> DescribeStateMachineAllocationLatitude()
    {
        // Whether this async method's state machine is heap-allocated or
        // stack-allocated/pooled by the runtime is never asserted.
        await Task.Yield();
        return 1;
    }

    public static async Task<string> DescribeSynchronizationContextLatitude()
    {
        var before = SynchronizationContext.Current;
        await Task.Yield();
        var after = SynchronizationContext.Current;

        // Never asserts the two must be equal or of a particular type.
        return $"synchronization-context-observed-before-null={before is null} synchronization-context-observed-after-null={after is null}";
    }

    public static async Task<int> DescribeThreadInterleavingLatitude()
    {
        var counter = 0;
        var tasks = Enumerable.Range(0, 4).Select(async _ =>
        {
            await Task.Yield();
            Interlocked.Increment(ref counter);
        });

        // Only the final aggregate is asserted, never the interleaving order
        // among the four tasks.
        await Task.WhenAll(tasks);
        return counter;
    }
}
