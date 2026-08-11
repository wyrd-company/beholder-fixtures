namespace Catalog.FunctionsAndAsync.Exceptions;

public sealed class SampleException : Exception
{
    public SampleException(string message) : base(message) { }
}

public sealed class AnotherSampleException : Exception
{
    public AnotherSampleException(string message) : base(message) { }
}

public static class ExceptionFilterCatalog
{
    private static bool ShouldHandle(SampleException ex) => ex.Message.Length > 0;

    private static bool SideEffectingFilter(SampleException ex, Action onEvaluated)
    {
        onEvaluated();
        return ex.Message.Contains("handle");
    }

    public static int TypedCatches(int value)
    {
        try
        {
            ThrowForValue(value);
            return 0;
        }
        catch (SampleException ex) when (ex.Message.Length > 0)
        {
            return 1;
        }
        catch (AnotherSampleException)
        {
            return 2;
        }
        catch (Exception)
        {
            return 3;
        }
    }

    public static int SideEffectingFilterCatch(int value, Action onFilterEvaluated)
    {
        try
        {
            throw new SampleException(value.ToString());
        }
        catch (SampleException ex) when (SideEffectingFilter(ex, onFilterEvaluated))
        {
            return 10;
        }
        catch (SampleException)
        {
            return 20;
        }
    }

    public static int FilterExceptionTreatedAsFalse(int value)
    {
        try
        {
            throw new SampleException("no-handle");
        }
        catch (SampleException ex) when (ThrowsInFilter(ex))
        {
            return 1;
        }
        catch (SampleException)
        {
            return 2;
        }
    }

    private static bool ThrowsInFilter(SampleException ex)
    {
        throw new InvalidOperationException("filter failure");
    }

    public static int NestedTryFinally(int value, Action onFinally)
    {
        int result = 0;
        try
        {
            try
            {
                if (value < 0)
                {
                    throw new SampleException("inner");
                }

                result = 100;
            }
            catch (SampleException)
            {
                result = 200;
                throw;
            }
            finally
            {
                onFinally();
            }
        }
        catch (SampleException)
        {
            result += 1000;
        }

        return result;
    }

    public static int ThrowVersusThrowEx(int value)
    {
        try
        {
            try
            {
                throw new SampleException($"origin:{value}");
            }
            catch (SampleException)
            {
                throw;
            }
        }
        catch (SampleException ex)
        {
            return ex.Message.Length;
        }
    }

    public static int ThrowExResetsStack(int value)
    {
        try
        {
            try
            {
                throw new SampleException($"first:{value}");
            }
            catch (SampleException ex)
            {
#pragma warning disable CA2200
                throw ex;
#pragma warning restore CA2200
            }
        }
        catch (SampleException ex)
        {
            bool hasStack = ex.StackTrace is not null;
            return hasStack ? 1 : 0;
        }
    }

    public static int ExceptionInFinally(int value, Action onFinally)
    {
        try
        {
            try
            {
                if (value == 0)
                {
                    throw new SampleException("try");
                }

                return 0;
            }
            finally
            {
                onFinally();
                throw new AnotherSampleException("finally");
            }
        }
        catch (AnotherSampleException)
        {
            return 777;
        }
    }

    public static async Task<int> AsyncExceptionTiming(int value)
    {
        try
        {
            await Task.Delay(1);
            if (value < 0)
            {
                throw new SampleException("async");
            }

            return value;
        }
        catch (SampleException)
        {
            return -1;
        }
    }

    public static int IteratorExceptionTiming(int value)
    {
        int sum = 0;
        try
        {
            foreach (int v in IteratorThatThrows(value))
            {
                sum += v;
            }
        }
        catch (SampleException)
        {
            sum += 1000;
        }

        return sum;
    }

    private static IEnumerable<int> IteratorThatThrows(int value)
    {
        yield return 1;
        if (value < 0)
        {
            throw new SampleException("iterator");
        }

        yield return 2;
    }

    public static int UnreachableCatchAfterFilter(int value)
    {
        try
        {
            throw new SampleException("handle-me");
        }
        catch (SampleException ex) when (ShouldHandle(ex))
        {
            return 1;
        }
        catch (SampleException)
        {
            return 2;
        }
    }

    private static void ThrowForValue(int value)
    {
        if (value == 1)
        {
            throw new SampleException("sample");
        }

        if (value == 2)
        {
            throw new AnotherSampleException("another");
        }

        if (value == 3)
        {
            throw new InvalidOperationException("other");
        }
    }
}
