using System.Collections;

namespace Catalog.FunctionsAndAsync.Iterators;

public static class IteratorCatalog
{
    public static IEnumerable<int> GenericIterator(int count)
    {
        for (int i = 0; i < count; i++)
        {
            yield return i;
        }
    }

    public static IEnumerable GenericNonGenericIterator(int count)
    {
        for (int i = 0; i < count; i++)
        {
            yield return i * 2;
        }
    }

    public static IEnumerable<T> GenericIteratorOfT<T>(IReadOnlyList<T> source)
    {
        foreach (T item in source)
        {
            yield return item;
        }
    }

    public static IEnumerable<int> IteratorWithTryFinally(int count, Action onFinally)
    {
        try
        {
            for (int i = 0; i < count; i++)
            {
                yield return i;
            }
        }
        finally
        {
            onFinally();
        }
    }

    public static IEnumerable<int> IteratorWithDeferredException(int count)
    {
        for (int i = 0; i < count; i++)
        {
            if (i == 2)
            {
                throw new InvalidOperationException("deferred");
            }

            yield return i;
        }
    }

    public static IEnumerable<int> IteratorWithDisposal(Action onDispose)
    {
        try
        {
            yield return 1;
            yield return 2;
            yield return 3;
        }
        finally
        {
            onDispose();
        }
    }

    public static IEnumerable<int> IteratorLocalFunctionWrapper(int count)
    {
        return Local();

        IEnumerable<int> Local()
        {
            for (int i = 0; i < count; i++)
            {
                yield return i + 10;
            }
        }
    }

    public static int RepeatedEnumerationCount(int count)
    {
        IEnumerable<int> sequence = GenericIterator(count);
        int first = sequence.Count();
        int second = sequence.Count();
        return first + second;
    }

    public static IEnumerable<int> IteratorWithRefSafeRegion(int count)
    {
        for (int i = 0; i < count; i++)
        {
            int local = i * 3;
            yield return local;
        }
    }

    public static IEnumerable<int> IteratorWithUsingInside(int count)
    {
        using var tracker = new IteratorTracker();
        for (int i = 0; i < count; i++)
        {
            yield return i;
            tracker.Touch(i);
        }
    }

    public static IEnumerable<int> IteratorSideEffectTiming(int count, Action<int> onYield)
    {
        for (int i = 0; i < count; i++)
        {
            onYield(i);
            yield return i;
        }
    }
}

internal sealed class IteratorTracker : IDisposable
{
    public int Touched { get; private set; }

    public void Touch(int value) => Touched += value;

    public void Dispose() => Touched = -1;
}
