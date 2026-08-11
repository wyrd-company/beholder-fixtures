namespace Catalog.FunctionsAndAsync.CSharp13;

public static class LockAndRefHost
{
    public static int WithSpecializedLock(System.Threading.Lock gate, int value)
    {
        lock (gate)
        {
            return value * 2;
        }
    }

    public static IEnumerable<int> RefSafeIterator(int count)
    {
        for (int i = 0; i < count; i++)
        {
            int local = i * 2;
            yield return local;
        }
    }

    public static int WithEnterScope(System.Threading.Lock gate, Func<int> body)
    {
        using (gate.EnterScope())
        {
            return body();
        }
    }
}
