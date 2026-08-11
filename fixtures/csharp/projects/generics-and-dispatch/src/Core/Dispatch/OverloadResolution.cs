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

    // Optional versus params and receiver inheritance.
    public static string WithOptional(string name, int count = 1) => $"{name}:{count}";
    public static string WithParams(params string[] names) => string.Join(",", names);
    public static string WithParams(Span<string> names) => string.Join(",", names.ToArray());

    // Ref kind differentiation.
    public static string ByRef(ref int value) => $"ref:{value}";

    public static string ByRef(int value) => $"value:{value}";

    public static string WithIn(in int value) => $"in:{value}";

    // Lambda/method-group target competition.
    public static int Apply(Func<int, int> func, int value) => func(value);
    public static int Apply(Func<int, string> func, int value) => func(value).Length;

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

        // Optional versus params.
        string o1 = WithOptional("a");
        string o2 = WithOptional("a", 2);
        string p1 = WithParams("a", "b");
        string p2 = WithParams(["a", "b"]);
        string p3 = WithParams();

        // Ref kind overloads resolved by call-site modifier.
        int number = 5;
        int snapshot = number;
        string b1 = ByRef(snapshot);
        string b2 = ByRef(ref number);
        string b3 = WithIn(in snapshot);

        // Lambda target competition disambiguated by explicit target type.
        int l1 = Apply((int x) => x * 2, 7);
        Func<int, int> target = static x => x + 1;
        int l2 = Apply(target, 7);
        int l3 = Apply((Func<int, int>)(static x => x + 2), 7);

        // Method group target.
        int m1 = Apply(Scale, 3);

        _ = r1; _ = r2; _ = r3; _ = r4; _ = r5; _ = r6; _ = r7;
        _ = o1; _ = o2; _ = p1; _ = p2; _ = p3;
        _ = b1; _ = b2; _ = b3;
        _ = l1; _ = l2; _ = l3; _ = m1;
    }

    private static int Scale(int value) => value * 3;
    private static string ScaleString(int value) => value.ToString();
}

public static class ExtensionOverloads
{
    public static int Extend(this string value, int pad) => value.Length + pad;
    public static int Extend(this object value, int pad) => -1;

    public static void Run()
    {
        string text = "hi";
        int instanceWins = text.Length;
        int extensionChosen = text.Extend(2);
        _ = instanceWins;
        _ = extensionChosen;
    }
}
