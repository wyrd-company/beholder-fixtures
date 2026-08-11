using System.Collections;
using System.Runtime.CompilerServices;
using System.Text;

namespace Fixture.AttributesAndMetadata.Core.Recognized;

/// <summary>
/// A custom interpolated-string handler recognized via
/// <see cref="InterpolatedStringHandlerAttribute"/>; the compiler routes
/// matching interpolated-string arguments through
/// <see cref="AppendLiteral"/>/<see cref="AppendFormatted{T}"/> instead of
/// calling <see cref="string.Format(string, object?[])"/>.
/// </summary>
[InterpolatedStringHandler]
public ref struct ShowcaseInterpolatedHandler
{
    private readonly StringBuilder _builder;

    public ShowcaseInterpolatedHandler(int literalLength, int formattedCount)
    {
        _builder = new StringBuilder(literalLength);
    }

    public void AppendLiteral(string value) => _builder.Append(value);

    public void AppendFormatted<T>(T value) => _builder.Append(value);

    public override readonly string ToString() => _builder.ToString();
}

public static class HandlerDemo
{
    public static string Render(ShowcaseInterpolatedHandler handler) => handler.ToString();

    public static string RenderSample(int quantity) => Render($"quantity={quantity}, doubled={quantity * 2}");
}

/// <summary>
/// A custom collection type recognized via
/// <see cref="CollectionBuilderAttribute"/>, constructible from a collection
/// expression.
/// </summary>
[CollectionBuilder(typeof(ShowcaseCollectionBuilder), nameof(ShowcaseCollectionBuilder.Create))]
public sealed class ShowcaseCollection : IEnumerable<int>
{
    private readonly int[] _items;

    internal ShowcaseCollection(int[] items) => _items = items;

    public IEnumerator<int> GetEnumerator() => ((IEnumerable<int>)_items).GetEnumerator();

    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
}

public static class ShowcaseCollectionBuilder
{
    public static ShowcaseCollection Create(ReadOnlySpan<int> items) => new(items.ToArray());
}

public static class CollectionBuilderDemo
{
    public static ShowcaseCollection BuildViaCollectionExpression()
    {
        ShowcaseCollection collection = [1, 2, 3];
        return collection;
    }
}

/// <summary>
/// A custom task-like type recognized via
/// <see cref="AsyncMethodBuilderAttribute"/>, whose builder forwards to
/// <see cref="AsyncTaskMethodBuilder"/>.
/// </summary>
[AsyncMethodBuilder(typeof(ShowcaseTaskMethodBuilder))]
public readonly struct ShowcaseTask
{
    internal readonly Task Inner;

    internal ShowcaseTask(Task inner) => Inner = inner;

    public ShowcaseTaskAwaiter GetAwaiter() => new(Inner.GetAwaiter());
}

public readonly struct ShowcaseTaskAwaiter : ICriticalNotifyCompletion
{
    private readonly TaskAwaiter _inner;

    internal ShowcaseTaskAwaiter(TaskAwaiter inner) => _inner = inner;

    public bool IsCompleted => _inner.IsCompleted;

    public void GetResult() => _inner.GetResult();

    public void OnCompleted(Action continuation) => _inner.OnCompleted(continuation);

    public void UnsafeOnCompleted(Action continuation) => _inner.UnsafeOnCompleted(continuation);
}

public struct ShowcaseTaskMethodBuilder
{
    private AsyncTaskMethodBuilder _inner;

    public static ShowcaseTaskMethodBuilder Create() => new() { _inner = AsyncTaskMethodBuilder.Create() };

    public void Start<TStateMachine>(ref TStateMachine stateMachine)
        where TStateMachine : IAsyncStateMachine
        => _inner.Start(ref stateMachine);

    public void SetStateMachine(IAsyncStateMachine stateMachine) => _inner.SetStateMachine(stateMachine);

    public void SetResult() => _inner.SetResult();

    public void SetException(Exception exception) => _inner.SetException(exception);

    public readonly ShowcaseTask Task => new(_inner.Task);

    public void AwaitOnCompleted<TAwaiter, TStateMachine>(ref TAwaiter awaiter, ref TStateMachine stateMachine)
        where TAwaiter : INotifyCompletion
        where TStateMachine : IAsyncStateMachine
        => _inner.AwaitOnCompleted(ref awaiter, ref stateMachine);

    public void AwaitUnsafeOnCompleted<TAwaiter, TStateMachine>(ref TAwaiter awaiter, ref TStateMachine stateMachine)
        where TAwaiter : ICriticalNotifyCompletion
        where TStateMachine : IAsyncStateMachine
        => _inner.AwaitUnsafeOnCompleted(ref awaiter, ref stateMachine);
}

public static class AsyncBuilderDemo
{
    public static async ShowcaseTask AnnounceAsync()
    {
        await Task.Yield();
    }
}
