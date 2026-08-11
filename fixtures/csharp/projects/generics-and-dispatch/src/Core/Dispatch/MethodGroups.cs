using System.Linq.Expressions;

namespace GenericsAndDispatch.Core.Dispatch;

public static class MethodGroupSamples
{
    public static int Scale(int value) => value * 2;
    public static int Scale(int left, int right) => left * right;
    public static void Log(string message) => _ = message;
}

public sealed class Worker
{
    public int Factor { get; init; }
    public Worker(int factor) => Factor = factor;
    public int Apply(int value) => value * Factor;
    public static int ApplyStatic(int value) => value + 1;
}

public static class MethodGroupExercises
{
    public static void Run()
    {
        var worker = new Worker(3);

        // Overloaded method group to delegate (target typing disambiguates).
        Func<int, int> single = MethodGroupSamples.Scale;
        Func<int, int, int> binary = MethodGroupSamples.Scale;

        // Equivalent lambdas assigned to same delegate shapes.
        Func<int, int> lambdaSingle = x => x * 2;
        Func<int, int, int> lambdaBinary = (l, r) => l * r;

        // Extension candidate as method group: Enumerable.Select.
        Func<IEnumerable<int>, Func<int, int>, IEnumerable<int>> selector = Enumerable.Select;

        // Static versus instance capture.
        Func<int, int> instance = worker.Apply;
        Func<int, int> capturingLambda = value => worker.Apply(value);
        Func<int, int> staticTarget = Worker.ApplyStatic;
        Func<int, int> nonCapturing = static value => value + 5;

        // Variance: delegate with variant parameter accepts more derived method group.
        Action<object> objectSink = static obj => { _ = obj; };
        Action<string> stringSink = objectSink;

        // Target-typed conditional, default, and new.
        Func<int, int> conditional = true ? single : lambdaSingle;
        Func<int, int>? maybeNull = default;
        Worker created = new(7);

        // Natural function types: var with lambda gets natural delegate type.
        var natural = (int x) => x + 1;
        Func<int, int> fromNatural = natural;

        // Method group to expression tree versus delegate.
        Expression<Func<int, int>> expression = x => x * 2;
        Func<int, int> compiled = expression.Compile();

        // Ref signature mismatch not valid; valid ref-like method group shown via overload set above.

        _ = single(3);
        _ = binary(2, 3);
        _ = lambdaSingle(3);
        _ = lambdaBinary(2, 3);
        _ = selector([1, 2, 3], single).ToArray();
        _ = instance(4);
        _ = capturingLambda(4);
        _ = staticTarget(4);
        _ = nonCapturing(4);
        stringSink("text");
        _ = conditional(5);
        _ = maybeNull;
        _ = created;
        _ = fromNatural(5);
        _ = compiled(5);
    }
}

public static class ExtensionMethodGroups
{
    public static int SumAll(this IEnumerable<int> source) => source.Sum();
    public static void Run()
    {
        IEnumerable<int> values = [1, 2, 3];
        Func<IEnumerable<int>, int> group = SumAll;
        int viaGroup = group(values);
        int viaCall = values.SumAll();
        _ = viaGroup;
        _ = viaCall;
    }
}
