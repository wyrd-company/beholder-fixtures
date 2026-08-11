namespace Bakery.TypesAndValues.Core.Tuples;

// CS-CAN-025: tuples — named, unnamed, inferred-name, converted, deconstructed,
// nested 8+ element, dynamic-element, nullable-element tuples in public and local APIs.

public static class TupleShapes
{
    public static (int, string) Unnamed() => (42, "sourdough");

    public static (int Count, string Label) Named() => (Count: 6, Label: "rye");

    public static (int Count, string Label) InferredName()
    {
        int count = 3;
        string label = "baguette";
        return (count, label);
    }

    public static (object First, string Label) Converted()
    {
        (int Count, string Label) named = Named();
        (object, string) converted = ((object)named.Count, named.Label);
        (int, string) unnamed = named;
        _ = unnamed;
        return (converted.Item1, converted.Item2);
    }

    public static (int Sum, string Combined) Deconstructed()
    {
        (int Count, string Label) tuple = Named();
        var (count, label) = tuple;
        return (count + 1, label + "-batch");
    }

    public static (int a, int b, int c, int d, int e, int f, int g, int h) EightPlus()
    {
        return (1, 2, 3, 4, 5, 6, 7, 8);
    }

    public static (int a, int b, int c, int d, int e, int f, int g, int h, int i) NineElements()
    {
        // Eight+ elements: the 8th position is the nested Rest tuple.
        var tuple = (1, 2, 3, 4, 5, 6, 7, 8, 9);
        _ = tuple.Rest;
        return tuple;
    }

    public static (dynamic Value, string Label) DynamicElement()
    {
        dynamic value = 42;
        return (value, "dynamic-batch");
    }

    public static (string? Label, int? Count) NullableElement() => (null, 5);

    public static bool ErasedNamesAreSameRuntimeType()
    {
        (int X, int Y) first = (1, 2);
        (int A, int B) second = (3, 4);
        return first.GetType() == second.GetType();
    }

    public static bool NameMismatchWarningDemo()
    {
        (int Count, string Label) named = (Count: 1, Label: "a");
        // Assignment with different element names still compiles with a warning
        // about element name mismatch; runtime identity is unchanged.
#pragma warning disable CS8123
        (int Total, string Name) renamed = named;
#pragma warning restore CS8123
        _ = renamed;
        return named.GetType() == renamed.GetType();
    }

    public static bool Equality((int, string) left, (int, string) right) => left == right;

    public static bool Inequality((int Count, string Label) left, (int Count, string Label) right) =>
        left != right;

    public static (int, string) ReturnAsUnnamed((int Count, string Label) named) => named;

    public static void ConsumeAsNamed((int, string) unnamed)
    {
        (int Count, string Label) named = unnamed;
        _ = named.Count;
    }

    public static (int Sum, int Product) DeconstructNested(
        (int a, (int b, int c) inner) tuple)
    {
        var (a, (b, c)) = tuple;
        return (a + b + c, a * b);
    }

    public static string DescribeViaDeconstruction((int Count, string Label) tuple)
    {
        var (count, label) = tuple;
        return $"{label}:{count}";
    }

    // Public API with tuple in signature — metadata encodes TupleElementNames via
    // TupleElementNamesAttribute when names are present.
    public static (int Count, string Label) PublicApi((int Count, string Label) input) => input;
}
