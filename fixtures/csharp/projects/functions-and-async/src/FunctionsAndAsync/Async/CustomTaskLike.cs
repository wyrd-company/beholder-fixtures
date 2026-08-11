using System.Runtime.CompilerServices;

namespace Catalog.FunctionsAndAsync.Async;

[AsyncMethodBuilder(typeof(PooledTaskBuilder<>))]
public sealed class PooledTask<T>
{
    private readonly Task<T> _inner;

    public PooledTask(Task<T> inner) => _inner = inner;

    public Task<T> AsTask() => _inner;

    public Awaiter GetAwaiter() => new(_inner);

    public sealed class Awaiter : INotifyCompletion
    {
        private readonly Task<T> _task;

        public Awaiter(Task<T> task) => _task = task;

        public bool IsCompleted => _task.IsCompleted;

        public T GetResult() => _task.GetAwaiter().GetResult();

        public void OnCompleted(Action continuation) =>
            _task.ConfigureAwait(false).GetAwaiter().OnCompleted(continuation);
    }
}

public sealed class PooledTaskBuilder<T>
{
    private AsyncTaskMethodBuilder<T> _inner = AsyncTaskMethodBuilder<T>.Create();

    public static PooledTaskBuilder<T> Create() => new();

    public void Start<TStateMachine>(ref TStateMachine stateMachine)
        where TStateMachine : IAsyncStateMachine => _inner.Start(ref stateMachine);

    public void SetStateMachine(IAsyncStateMachine stateMachine) => _inner.SetStateMachine(stateMachine);

    public void SetResult(T result) => _inner.SetResult(result);

    public void SetException(Exception exception) => _inner.SetException(exception);

    public PooledTask<T> Task => new(_inner.Task);

    public void AwaitOnCompleted<TAwaiter, TStateMachine>(ref TAwaiter awaiter, ref TStateMachine stateMachine)
        where TAwaiter : INotifyCompletion
        where TStateMachine : IAsyncStateMachine =>
        _inner.AwaitOnCompleted(ref awaiter, ref stateMachine);

    public void AwaitUnsafeOnCompleted<TAwaiter, TStateMachine>(ref TAwaiter awaiter, ref TStateMachine stateMachine)
        where TAwaiter : ICriticalNotifyCompletion
        where TStateMachine : IAsyncStateMachine =>
        _inner.AwaitUnsafeOnCompleted(ref awaiter, ref stateMachine);
}
