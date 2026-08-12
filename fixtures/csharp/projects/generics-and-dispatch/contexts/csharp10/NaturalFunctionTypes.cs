namespace GenericsAndDispatch.CSharp10;

public static class NaturalFunctionTypes
{
    public static void Run()
    {
        // Natural type inferred for lambda without target type.
        var add = (int x, int y) => x + y;
        Func<int, int, int> asFunc = add;
        var inferred = (string s) => s.Length;

        // Explicit target type versus natural.
        Func<int, string> explicitTarget = x => x.ToString();
        var naturalLambda = (int x) => x.ToString();

        // Method group natural handling via var.
        var naturalGroup = Transform;
        var methodGroup = (int x) => Transform(x);
        Func<int, int> groupAsDelegate = Transform;

        // Target-typed conditional and default.
        Func<int, int, int> conditional = true ? add : (int x, int y) => x * y;
        Func<int, int>? maybe = default;

        // Overload that differs by delegate shape exercised via natural lambdas.
        int r1 = Apply((int x) => x + 1, 5);
        int r2 = Apply((string s) => s.Length, "hello");

        _ = asFunc(1, 2);
        _ = inferred("test");
        _ = explicitTarget(5);
        _ = naturalLambda(3);
        _ = naturalGroup(3);
        _ = methodGroup(3);
        _ = groupAsDelegate(3);
        _ = conditional(2, 3);
        _ = add(1, 2);
        _ = maybe;
        _ = r1;
        _ = r2;
    }

    private static int Transform(int value) => value * 2;

    private static int Apply(Func<int, int> func, int value) => func(value);
    private static int Apply(Func<string, int> func, string value) => func(value);
}
