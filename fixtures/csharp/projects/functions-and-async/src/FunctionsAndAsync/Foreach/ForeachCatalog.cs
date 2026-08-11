namespace Catalog.FunctionsAndAsync.Foreach;

public static class ForeachCatalog
{
    public static int OverArray(int[] values)
    {
        int sum = 0;
        foreach (int v in values)
        {
            sum += v;
        }

        return sum;
    }

    public static int OverString(string text)
    {
        int count = 0;
        foreach (char ch in text)
        {
            count += ch;
        }

        return count;
    }

    public static int OverListWithStructEnumerator(List<int> values)
    {
        int sum = 0;
        foreach (int v in values)
        {
            sum += v;
        }

        return sum;
    }

    public static int OverPatternOnly(PatternOnlyCollection collection)
    {
        int sum = 0;
        foreach (int v in collection)
        {
            sum += v;
        }

        return sum;
    }

    public static int OverExtensionGetEnumerator(PlainCollection collection)
    {
        int sum = 0;
        foreach (int v in collection)
        {
            sum += v;
        }

        return sum;
    }

    public static int OverSpan(Span<int> span)
    {
        int sum = 0;
        foreach (int v in span)
        {
            sum += v;
        }

        return sum;
    }

    public static int OverSpanWithRef(Span<int> span)
    {
        int sum = 0;
        foreach (ref int v in span)
        {
            v += 1;
            sum += v;
        }

        return sum;
    }

    public static int OverSpanWithRefReadonly(ReadOnlySpan<int> span)
    {
        int sum = 0;
        foreach (ref readonly int v in span)
        {
            sum += v;
        }

        return sum;
    }

    public static int WithImplicitConversion(IEnumerable<object> source)
    {
        int sum = 0;
        foreach (string s in source)
        {
            sum += s.Length;
        }

        return sum;
    }

    public static int WithBreakAndDisposal(DisposablePatternCollection collection)
    {
        int sum = 0;
        foreach (int v in collection)
        {
            sum += v;
            if (v == 2)
            {
                break;
            }
        }

        return sum;
    }

    public static int WithExceptionAndDisposal(DisposablePatternCollection collection)
    {
        int sum = 0;
        try
        {
            foreach (int v in collection)
            {
                if (v == 99)
                {
                    throw new InvalidOperationException("stop");
                }

                sum += v;
            }
        }
        catch (InvalidOperationException)
        {
            sum += 1000;
        }

        return sum;
    }

    public static int OverStructCollection(StructEnumeratorCollection collection)
    {
        int sum = 0;
        foreach (int v in collection)
        {
            sum += v;
        }

        return sum;
    }

    public static int OverRefStructPattern(RefStructPatternCollection collection)
    {
        int sum = 0;
        foreach (int v in collection)
        {
            sum += v;
        }

        return sum;
    }

    public static int OverBoxingStruct(BoxingStructCollection collection)
    {
        int sum = 0;
        foreach (int v in collection)
        {
            sum += v;
        }

        return sum;
    }

    public static int OverDynamic(dynamic collection)
    {
        int sum = 0;
        foreach (int v in collection)
        {
            sum += v;
        }

        return sum;
    }
}
