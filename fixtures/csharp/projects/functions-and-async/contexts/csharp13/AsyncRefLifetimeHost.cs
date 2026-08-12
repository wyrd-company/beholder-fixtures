namespace Catalog.FunctionsAndAsync.CSharp13;

// C# 13 permits ref struct locals (for example Span<T>) and ref locals inside
// async methods, provided the value does not remain alive across an await
// suspension point. Both members below confine the ref-like value to a region
// that completes before the first await, which earlier LangVersion selections
// reject outright.
public static class AsyncRefLifetimeHost
{
    public static async Task<int> SpanNotCrossingSuspension(int[] buffer)
    {
        Span<int> span = buffer;
        int sum = 0;
        for (int i = 0; i < span.Length; i++)
        {
            sum += span[i];
        }

        await Task.Delay(1);
        return sum;
    }

    public static async Task<int> RefLocalNotCrossingSuspension(int value)
    {
        int local = value * 2;
        ref int r = ref local;
        int before = r + 1;
        await Task.Delay(1);
        return before;
    }
}
