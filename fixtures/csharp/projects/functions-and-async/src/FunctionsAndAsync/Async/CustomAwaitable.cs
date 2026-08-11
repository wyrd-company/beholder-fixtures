using System.Runtime.CompilerServices;

namespace Catalog.FunctionsAndAsync.Async;

public sealed class CustomAwaitable
{
    private readonly int _value;

    public CustomAwaitable(int value) => _value = value;

    public CustomAwaiter GetAwaiter() => new(_value);
}

public struct CustomAwaiter : INotifyCompletion
{
    private readonly int _value;

    public CustomAwaiter(int value) => _value = value;

    public bool IsCompleted => true;

    public int GetResult() => _value;

    public void OnCompleted(Action continuation) => continuation();
}

public static class CustomAwaitableExtensions
{
    public static CustomAwaiter GetAwaiter(this int value) => new(value * 2);
}
