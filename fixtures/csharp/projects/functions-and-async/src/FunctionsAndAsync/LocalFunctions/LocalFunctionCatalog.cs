namespace Catalog.FunctionsAndAsync.LocalFunctions;

public static class LocalFunctionCatalog
{
    public static int ForwardCalledGenericRecursive(int n)
    {
        return Factorial(n);

        T Identity<T>(T value) => value;

        int Factorial(int value)
        {
            if (value <= 1)
            {
                return Identity(1);
            }

            return value * Factorial(value - 1);
        }
    }

    public static int UseStaticLocalFunction(int value)
    {
        return Triple(value);

        static int Triple(int x) => x * 3;
    }

    public static Func<int, int> CapturedLocalFunction(int offset)
    {
        int AddOffset(int x) => x + offset;
        return AddOffset;
    }

    public static IEnumerable<int> IteratorLocalFunction(int count)
    {
        return Produce();

        IEnumerable<int> Produce()
        {
            for (int i = 0; i < count; i++)
            {
                yield return i * 2;
            }
        }
    }

    public static async Task<int> AsyncLocalFunction(int value)
    {
        return await AddAsync(value);

        async Task<int> AddAsync(int x)
        {
            await Task.Delay(1);
            return x + 10;
        }
    }

    public static int AttributedLocalFunction(int value)
    {
        return Marked(value);

        [SampleMarker("local")]
        int Marked(int x) => x + 7;
    }

    public static int GenericRecursiveWithOverload(int n)
    {
        _ = Echo(42);
        return Count(n);

        int Count(int remaining)
        {
            if (remaining <= 0)
            {
                return 0;
            }

            return 1 + Count(remaining - 1);
        }

        T Echo<T>(T input) => input;
    }

    public static int LexicalScopeAndDefiniteAssignment(bool flag)
    {
        int result;
        if (flag)
        {
            result = WithAssignment();
        }
        else
        {
            result = WithoutAssignment();
        }

        return result;

        int WithAssignment() => 1;
        int WithoutAssignment() => 2;
    }

    public static int StaticGenericLocalFunction<T>(T value, Func<T, int> projector)
    {
        int Project(T inner) => ProjectWithCapture(inner, projector);
        static int ProjectWithCapture(T inner, Func<T, int> fn) => fn(inner);
        return Project(value);
    }
}

[AttributeUsage(AttributeTargets.All)]
internal sealed class SampleMarkerAttribute : Attribute
{
    public SampleMarkerAttribute(string tag) => Tag = tag;
    public string Tag { get; }
}
