namespace Catalog.FunctionsAndAsync.Locking;

public static class LockCatalog
{
    public static int MonitorLock(object sync, Func<int> body)
    {
        lock (sync)
        {
            return body();
        }
    }

    public static int MonitorLockWithReturn(object sync, int value)
    {
        lock (sync)
        {
            if (value < 0)
            {
                return -1;
            }

            return value * 2;
        }
    }

    public static int MonitorLockWithException(object sync, int value)
    {
        try
        {
            lock (sync)
            {
                if (value < 0)
                {
                    throw new InvalidOperationException("negative");
                }

                return value;
            }
        }
        catch (InvalidOperationException)
        {
            return -99;
        }
    }

    public static int SpecializedLock(System.Threading.Lock sync, Func<int> body)
    {
        lock (sync)
        {
            return body();
        }
    }

    public static int SpecializedLockWithReturn(System.Threading.Lock sync, int value)
    {
        lock (sync)
        {
            if (value == 0)
            {
                return 0;
            }

            return value + 10;
        }
    }

    public static int SpecializedLockWithException(System.Threading.Lock sync, int value)
    {
        try
        {
            lock (sync)
            {
                if (value < 0)
                {
                    throw new InvalidOperationException("negative-lock");
                }

                return value;
            }
        }
        catch (InvalidOperationException)
        {
            return -100;
        }
    }

    public static async Task<int> LockScopeDoesNotCrossAwait(object sync, int value)
    {
        int inside;
        lock (sync)
        {
            inside = value * 2;
        }

        await Task.Delay(1);
        return inside + 1;
    }

    public static int LockWithConversionToObject(System.Threading.Lock typedLock, Func<int> body)
    {
#pragma warning disable CS9216
        object asObject = typedLock;
        lock (asObject)
        {
            return body();
        }
#pragma warning restore CS9216
    }

    public static int BoxingValueTypeTrap(int value, Func<int> body)
    {
        object boxed = value;
        lock (boxed)
        {
            return body();
        }
    }
}
