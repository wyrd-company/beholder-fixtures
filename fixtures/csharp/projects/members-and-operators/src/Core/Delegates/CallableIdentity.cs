namespace Catalog.Core.Delegates;

public delegate int PairTransform(int left, int right);

public delegate void NoticeHandler(string message);

public delegate T SelfMap<T>(T value);

public delegate T CovariantFactory<out T>(int seed);

public delegate void ContravariantSink<in T>(T value);

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

    public static bool CompareDelegateIdentity(Worker worker)
    {
        Action<int> methodGroup = worker.Apply;
        Action<int> lambda = value => worker.Apply(value);
        bool referencesDiffer = !ReferenceEquals(methodGroup, lambda);
        bool targetsDiffer = methodGroup != lambda;
        return referencesDiffer && targetsDiffer;
    }

    public static int RemoveLastMatchingSubsequence(
        PairTransform first,
        PairTransform second,
        PairTransform third,
        int left,
        int right)
    {
        PairTransform multicast = first + second + third + second;
        multicast = (PairTransform)Delegate.Remove(multicast, second)!;
        return multicast(left, right);
    }

    public static int InvokeThrowingMulticast(
        PairTransform safe,
        PairTransform throwing,
        int left,
        int right)
    {
        PairTransform multicast = safe + throwing;
        try
        {
            return multicast(left, right);
        }
        catch (InvalidOperationException)
        {
            return -1;
        }
    }

    public static int SelectByTargetSignature(Worker worker, int left, int right)
    {
        PairTransform binary = worker.Transform;
        Func<int, int> unary = worker.Echo;
        return binary(left, right) + unary(left);
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

    public int Echo(int value) => value;

    public static int ThrowingTransform(int left, int right) =>
        throw new InvalidOperationException("multicast target");
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
