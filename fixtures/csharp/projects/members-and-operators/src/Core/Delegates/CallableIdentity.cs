namespace Catalog.Core.Delegates;

public delegate int PairTransform(int left, int right);

public delegate void NoticeHandler(string message);

public delegate T SelfMap<T>(T value);

public static class CallableIdentity
{
    public static int CombineAndInvoke(
        PairTransform first,
        PairTransform second,
        int left,
        int right)
    {
        PairTransform? multicast = first + second;
        multicast = (PairTransform?)Delegate.Remove(multicast, first);
        multicast = (PairTransform?)Delegate.Combine(multicast, second);
        return multicast!(left, right);
    }

    public static void BindTargets(Worker worker, GridPoint point)
    {
        NoticeHandler staticTarget = StaticNotice;
        NoticeHandler instanceTarget = worker.RaiseNotice;
        Action<int> methodGroup = worker.Apply;
        Action<int> lambda = value => worker.Apply(value);
        NoticeHandler boxedStruct = point.Signal;

        NoticeHandler combined = staticTarget + instanceTarget + boxedStruct;
        combined = (NoticeHandler)Delegate.Remove(combined, staticTarget)!;
        combined.Invoke("ready");
        methodGroup(3);
        lambda(4);
    }

    private static void StaticNotice(string message)
    {
        _ = message;
    }
}

public sealed class Worker
{
    public void RaiseNotice(string message) => _ = message;

    public void Apply(int value) => _ = value;

    public int Transform(int left, int right) => left + right;
}

public struct GridPoint
{
    public int X;
    public int Y;

    public GridPoint(int x, int y)
    {
        X = x;
        Y = y;
    }

    public void Signal(string message) => _ = message;
}

public sealed class AsyncReturningDelegateHost
{
    public delegate Task<int> AsyncCompute(int seed);

    public static async Task<int> Run(AsyncCompute compute, int seed) => await compute(seed);
}
