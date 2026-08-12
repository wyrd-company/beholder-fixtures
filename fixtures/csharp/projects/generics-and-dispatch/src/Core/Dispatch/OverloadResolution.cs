namespace GenericsAndDispatch.Core.Dispatch;

public abstract class Shape
{
    public abstract double Area();
}

public sealed class Circle : Shape
{
    public double Radius { get; init; }
    public Circle(double radius) => Radius = radius;
    public override double Area() => Math.PI * Radius * Radius;
}

public sealed class Rectangle : Shape
{
    public double Width { get; init; }
    public double Height { get; init; }
    public Rectangle(double width, double height) => (Width, Height) = (width, height);
    public override double Area() => Width * Height;
}

public readonly struct Token
{
    public int Value { get; }
    public Token(int value) => Value = value;
    public static implicit operator int(Token token) => token.Value;
    public static implicit operator string(Token token) => token.Value.ToString();
}

public sealed class Extendable
{
    public int Extend(int pad) => 100 + pad;
}

public static class CatalogExtensionsForOverload
{
    public static int Extend(this Extendable value, int pad) => value.Extend(pad) + 1;
    public static int Extend(this string value, int pad) => value.Length + pad;
    public static int Extend(this object value, int pad) => -1;
}

public static class OverloadResolution
{
    // Numeric/reference conversion and inheritance distance.
    public static string Select(int value) => "int";
    public static string Select(double value) => "double";
    public static string Select(object value) => "object";
    public static string Select(Shape shape) => "shape";
    public static string Select(Circle circle) => "circle";

    // Genericity versus non-generic.
    public static string Select<T>(T value) => "generic";

    // Same-name optional versus params competing candidates.
    public static string Collect(string name, int count = 1) => $"{name}:{count}";
    public static string Collect(params string[] names) => string.Join(",", names);
    public static string Collect(Span<string> names) => string.Join(",", names.ToArray());

    // User-defined conversion overload set.
    public static string Accept(int value) => $"int:{value}";
    public static string Accept(string value) => $"string:{value}";
    public static string Accept(Token token) => $"token:{token.Value}";

    // Ref kind differentiation.
    public static string ByRef(ref int value) => $"ref:{value}";
    public static string ByRef(int value) => $"value:{value}";
    public static string WithIn(in int value) => $"in:{value}";

    // Lambda/method-group target competition.
    public static int Apply(Func<int, int> func, int value) => func(value);
    public static int Apply(Func<int, string> func, int value) => func(value).Length;

    // Target-typed collection, interpolation, span, and added-overload compatibility.
    public static int Process(IEnumerable<int> values) => values.Sum();
    public static int Process(int[] values) => values.Sum() + 1;
    public static int Process(ReadOnlySpan<int> values) => values.Length + 2;
    public static string Log(string message) => $"string:{message}";
    public static string Log(FormattableString message) => $"formattable:{message}";
    public static string Log(ReadOnlySpan<char> message) => $"span:{message.Length}";

    public static void Run()
    {
        // Numeric betterness: int prefers int overload.
        string r1 = Select(42);
        string r2 = Select(3.14);
        string r3 = Select("text");
        Shape shape = new Circle(2);
        string r4 = Select(shape);
        string r5 = Select(new Circle(1));
        string r6 = Select<string>("generic-wins");

        // Inheritance and conversion tie-breaking.
        Circle c = new(3);
        string r7 = Select((Shape)c);

        // Same-name optional versus params.
        string o1 = Collect("a");
        string o2 = Collect("a", 2);
        string p1 = Collect("a", "b");
        string p2 = Collect(["a", "b"]);
        string p3 = Collect();
        string ps = Collect(new Span<string>(["a", "b"]));

        // User-defined conversion overload set.
        Token token = new(5);
        string u1 = Accept(token);
        string u2 = Accept(5);
        string u3 = Accept("hi");
        string u4 = Accept((int)token);
        string u5 = Accept((string)token);

        // Ref kind overloads resolved by call-site modifier.
        int number = 5;
        int snapshot = number;
        string b1 = ByRef(snapshot);
        string b2 = ByRef(ref number);
        string b3 = WithIn(in snapshot);

        // Instance versus extension: instance wins.
        var extendable = new Extendable();
        int instanceWins = extendable.Extend(2);
        int extensionViaString = "hi".Extend(2);

        // Lambda target competition disambiguated by explicit target type.
        int l1 = Apply((int x) => x * 2, 7);
        Func<int, int> target = static x => x + 1;
        int l2 = Apply(target, 7);
        int l3 = Apply((Func<int, int>)(static x => x + 2), 7);

        // Method group target.
        int m1 = Apply(Scale, 3);

        // Target-typed collection, span, interpolation, compatibility.
        int t1 = Process([1, 2, 3]);
        int t2 = Process((int[])[1, 2, 3]);
        int t3 = Process((ReadOnlySpan<int>)[1, 2, 3]);
        int t4 = Process((IEnumerable<int>)[1, 2, 3]);
        string log1 = Log($"value:{42}");
        string log2 = Log((FormattableString)$"value:{42}");
        string log3 = Log((ReadOnlySpan<char>)"hello");

        // Added-overload compatibility across an assembly metadata boundary is modeled by the
        // versioned producer/consumer projects under compat/ (ConsumerV1 binds Render(object)
        // against version 1; ConsumerV2 rebinds to the added Render(string) against version 2).

        _ = r1; _ = r2; _ = r3; _ = r4; _ = r5; _ = r6; _ = r7;
        _ = o1; _ = o2; _ = p1; _ = p2; _ = p3; _ = ps;
        _ = u1; _ = u2; _ = u3; _ = u4; _ = u5;
        _ = b1; _ = b2; _ = b3;
        _ = instanceWins; _ = extensionViaString;
        _ = l1; _ = l2; _ = l3; _ = m1;
        _ = t1; _ = t2; _ = t3; _ = t4; _ = log1; _ = log2; _ = log3;
    }

    private static int Scale(int value) => value * 3;
}
