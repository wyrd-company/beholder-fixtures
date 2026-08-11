using System.Runtime.CompilerServices;

namespace Catalog.FunctionsAndAsync.AsyncIterators;

public static class AsyncStreamCatalog
{
    public static async IAsyncEnumerable<int> ProduceAsync(
        int count,
        [EnumeratorCancellation] CancellationToken token = default)
    {
        for (int i = 0; i < count; i++)
        {
            token.ThrowIfCancellationRequested();
            await Task.Delay(1, token);
            yield return i;
        }
    }

    public static async IAsyncEnumerable<int> ProduceWithAsyncDisposal(
        int count,
        [EnumeratorCancellation] CancellationToken token = default)
    {
        await using var resource = new AsyncTrackingResource();
        for (int i = 0; i < count; i++)
        {
            await Task.Delay(1, token);
            yield return i + resource.Offset;
        }
    }

    public static async Task<int> ConsumeAwaitForeach(int count)
    {
        int sum = 0;
        await foreach (int v in ProduceAsync(count))
        {
            sum += v;
        }

        return sum;
    }

    public static async Task<int> ConsumeWithCancellation(int count, CancellationToken token)
    {
        int sum = 0;
        await foreach (int v in ProduceAsync(count, token).WithCancellation(token))
        {
            sum += v;
        }

        return sum;
    }

    public static async Task<int> ConsumeCustomPattern(CustomAsyncSequence sequence)
    {
        int sum = 0;
        await foreach (int v in sequence)
        {
            sum += v;
        }

        return sum;
    }

    public static async Task<int> ConsumeWithConfigureAwait(int count)
    {
        int sum = 0;
        await foreach (int v in ProduceAsync(count).ConfigureAwait(false))
        {
            sum += v;
        }

        return sum;
    }

    public static async Task<int> MultipleEnumeration(int count)
    {
        var sequence = ProduceAsync(count);
        int first = 0;
        await foreach (int v in sequence)
        {
            first += v;
        }

        int second = 0;
        await foreach (int v in sequence)
        {
            second += v;
        }

        return first + second;
    }

    public static async Task<int> BreakDisposesAsyncEnumerator(int count)
    {
        int sum = 0;
        await foreach (int v in ProduceWithAsyncDisposal(count))
        {
            sum += v;
            if (v == 2)
            {
                break;
            }
        }

        return sum;
    }

    public static async Task<int> ExceptionDisposesAsyncEnumerator(int count)
    {
        int sum = 0;
        try
        {
            await foreach (int v in ProduceAsync(count))
            {
                if (v == 2)
                {
                    throw new InvalidOperationException("stop");
                }

                sum += v;
            }
        }
        catch (InvalidOperationException)
        {
            sum += 1000;
        }

        return sum;
    }

    public static async Task<int> AwaitUsingConsume(IAsyncDisposable resource, int count)
    {
        int sum = 0;
        await using (resource)
        {
            await foreach (int v in ProduceAsync(count))
            {
                sum += v;
            }
        }

        return sum;
    }
}

internal sealed class AsyncTrackingResource : IAsyncDisposable
{
    public int Offset => 10;
    public ValueTask DisposeAsync() => ValueTask.CompletedTask;
}

public sealed class CustomAsyncSequence
{
    private readonly int[] _values;

    public CustomAsyncSequence(params int[] values) => _values = values;

    public CustomAsyncEnumerator GetAsyncEnumerator(CancellationToken token = default) =>
        new(_values, token);
}

public sealed class CustomAsyncEnumerator : IAsyncEnumerator<int>
{
    private readonly int[] _values;
    private readonly CancellationToken _token;
    private int _index = -1;

    public CustomAsyncEnumerator(int[] values, CancellationToken token)
    {
        _values = values;
        _token = token;
    }

    public int Current => _values[_index];

    public ValueTask<bool> MoveNextAsync()
    {
        _token.ThrowIfCancellationRequested();
        _index++;
        return ValueTask.FromResult(_index < _values.Length);
    }

    public ValueTask DisposeAsync() => ValueTask.CompletedTask;
}
