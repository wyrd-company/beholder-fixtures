namespace Catalog.FunctionsAndAsync.Lambdas;

[AttributeUsage(AttributeTargets.All)]
internal sealed class SampleMarkerAttribute : Attribute
{
    public SampleMarkerAttribute(string tag) => Tag = tag;
    public string Tag { get; }
}

public sealed class Inventory
{
    public Inventory(int factor) => Factor = factor;
    public int Factor { get; }
    public int Scale(int value) => value * Factor;
}

public static class LambdaCaptureCatalog
{
    public static Func<int, int> CapturingLambda(int factor)
    {
        int local = factor + 1;
        return x => x * local;
    }

    public static Func<int, int> NonCapturingLambda()
    {
        return x => x * 2;
    }

    public static Func<int, int> StaticLambda()
    {
        return static x => x * 3;
    }

    public static Func<int, int> StaticLambdaCapturingParameter(int factor)
    {
        return static (x) => x * 2;
    }

    public static Func<int, int> AnonymousMethodCapturing(int offset)
    {
        Func<int, int> handler = delegate (int value)
        {
            return value + offset;
        };
        return handler;
    }

    public static Func<int, int> AnonymousMethodNonCapturing()
    {
        Func<int, int> handler = delegate (int value)
        {
            return value * 2;
        };
        return handler;
    }

    public static Func<int, int> AnonymousMethodStaticLike()
    {
        Func<int, int> handler = static delegate (int value)
        {
            return value * 3;
        };
        return handler;
    }

    public static Func<int, int> MutableCapture()
    {
        int counter = 0;
        Func<int, int> increment = x =>
        {
            counter++;
            return x + counter;
        };
        increment(0);
        increment(0);
        return increment;
    }

    public static List<Func<int>> LoopCapture(int count)
    {
        var handlers = new List<Func<int>>();
        for (int i = 0; i < count; i++)
        {
            int copy = i;
            handlers.Add(() => copy);
        }

        return handlers;
    }

    public static List<Func<int>> LoopCaptureWithForEach(IEnumerable<int> source)
    {
        var handlers = new List<Func<int>>();
        foreach (int item in source)
        {
            int copy = item;
            handlers.Add(() => copy);
        }

        return handlers;
    }

    public static Func<int, int> ThisCapture(Inventory inventory)
    {
        return x => inventory.Scale(x);
    }

    public static Func<int, int> ExplicitReturnTypeLambda()
    {
        Func<int, int> handler = int (int x) => x * 2;
        return handler;
    }

    public delegate int WithDefaultParam(int x = 5);

    public static WithDefaultParam DefaultParameterLambda()
    {
        WithDefaultParam handler = (int x = 5) => x * 2;
        return handler;
    }

    public static void NaturalTypeLambda()
    {
        var inferred = (int x) => x * 2;
        Func<int, int> typed = inferred;
        _ = typed(4);
    }

    public static Func<int, int> AttributedLambda()
    {
        Func<int, int> handler = [SampleMarker("lambda")] (int x) => x + 1;
        return handler;
    }

    public static Func<int, int> AttributedAnonymousMethod()
    {
        Func<int, int> handler = delegate (int x) { return x + 2; };
        return handler;
    }

    public static (Func<int>, Func<int>) SharedVariableLifetime()
    {
        int shared = 0;
        Func<int> reader = () => shared;
        Func<int> writer = () =>
        {
            shared++;
            return shared;
        };
        return (reader, writer);
    }

    public static Func<int, int> ClosureOverNestedScope(int outer)
    {
        Func<int, int> outerCapture = x => x + outer;
        int inner = outer * 2;
        Func<int, int> innerCapture = x => x + inner + outer;
        return x => outerCapture(x) + innerCapture(x);
    }
}
