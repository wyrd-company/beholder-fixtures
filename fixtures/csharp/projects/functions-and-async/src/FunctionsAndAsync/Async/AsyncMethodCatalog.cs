using System.Runtime.CompilerServices;

namespace Catalog.FunctionsAndAsync.Async;

public static class AsyncMethodCatalog
{
    public static async Task SimpleTask()
    {
        await Task.Delay(1);
    }

    public static async Task<int> SimpleTaskOfT(int value)
    {
        await Task.Delay(1);
        return value * 2;
    }

    public static async ValueTask<int> ValueTaskOfT(int value)
    {
        await Task.Delay(1);
        return value + 5;
    }

    public static async void AsyncVoid(Action<int> callback, int value)
    {
        await Task.Delay(1);
        callback(value);
    }

    public static async Task<int> SeveralAwaits(int value)
    {
        int a = await Task.FromResult(value + 1);
        int b = await new CustomAwaitable(a + 1);
        await Task.Yield();
        int c = await ValueTask.FromResult(b + 1);
        return c;
    }

    public static async Task<int> CustomAwaitableAwait(int value)
    {
        int result = await new CustomAwaitable(value * 3);
        return result;
    }

    public static async Task<int> ExtensionGetAwaiterAwait(int value)
    {
        int result = await value;
        return result;
    }

    public static async PooledTask<int> CustomTaskLikeAsync(int value)
    {
        await Task.Delay(1);
        return value * 4;
    }

    public static async PooledTask<int> CustomTaskLikeWithBuilderOverride(int value)
    {
        await Task.Yield();
        await Task.Delay(1);
        return value + 9;
    }

    public static async Task<int> ExceptionBeforeSuspension(int value)
    {
        if (value < 0)
        {
            throw new ArgumentOutOfRangeException(nameof(value));
        }

        await Task.Delay(1);
        return value;
    }

    public static async Task<int> ExceptionAfterSuspension(int value)
    {
        await Task.Delay(1);
        throw new InvalidOperationException($"after:{value}");
    }

#pragma warning disable CS1998
    public static async Task NoSuspensionWarning()
    {
        _ = 42;
    }
#pragma warning restore CS1998

    public static Func<Task<int>> AsyncLambda(int seed)
    {
        Func<Task<int>> handler = async () =>
        {
            await Task.Delay(1);
            return seed * 2;
        };
        return handler;
    }

    public static async Task<int> AwaitWithConfigureAwait(int value)
    {
        await Task.Delay(1).ConfigureAwait(false);
        return value;
    }

    public static async Task<int> RefSafeAcrossAwait(int value)
    {
        int local = value * 2;
        await Task.Delay(1);
        int after = local + 1;
        return after;
    }

    public static Task<int> AsyncEntryPointLike(string[] args)
    {
        return SimpleTaskOfT(args.Length);
    }

    public static async Task<int> WithCancellationAsync(int value, CancellationToken token)
    {
        await Task.Delay(10, token);
        token.ThrowIfCancellationRequested();
        return value;
    }
}
