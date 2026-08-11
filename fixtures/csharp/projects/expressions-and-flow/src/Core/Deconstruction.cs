namespace ExpressionsFlow.Core;

public sealed class Deconstructable
{
    public int X { get; }
    public int Y { get; }
    public string Label { get; }

    public Deconstructable(int x, int y, string label)
    {
        X = x;
        Y = y;
        Label = label;
    }

    public void Deconstruct(out int x, out int y)
    {
        x = X;
        y = Y;
    }

    public void Deconstruct(out int x, out int y, out string label)
    {
        x = X;
        y = Y;
        label = Label;
    }
}

public static class DeconstructableExtensions
{
    // Extension Deconstruct overloads by arity for external type
    public static void Deconstruct(this KeyValuePair<string, int> pair, out string key, out int value)
    {
        key = pair.Key;
        value = pair.Value;
    }
}

public sealed class AmbiguousArity
{
    public void Deconstruct(out int a) => a = 1;

    // Two Deconstruct with same arity would be ambiguous at call site:
    // public void Deconstruct(out int a) => a = 1;
    // public void Deconstruct(out string s) => s = "x";
    // The declaration above plus an extension with same arity creates candidate ambiguity,
    // demonstrated as a commented diagnostic below.
}

public static class Deconstruction
{
    // Tuple deconstruction
    public static (int Sum, int Product) TupleDeconstruction()
    {
        var (a, b) = (3, 4);
        return (a + b, a * b);
    }

    // Instance Deconstruct
    public static string InstanceDeconstruct()
    {
        var item = new Deconstructable(10, 20, "stock");
        var (x, y) = item;
        var (x2, y2, label) = item;
        return $"{x},{y},{x2},{y2},{label}";
    }

    // Extension Deconstruct
    public static string ExtensionDeconstruct()
    {
        var pair = new KeyValuePair<string, int>("alpha", 7);
        var (key, value) = pair;
        return $"{key}:{value}";
    }

    // Assignment to existing variables
    public static int ExistingVariables()
    {
        int a = 0, b = 0;
        (a, b) = (5, 6);
        return a + b;
    }

    // Mixed declarations: one existing, one new var
    public static int MixedDeclarations()
    {
        int existing = 1;
        (existing, var created) = (10, 20);
        return existing + created;
    }

    // Nested forms and discards
    public static int NestedAndDiscards()
    {
        var nested = (1, (2, 3));
        var (first, (second, _)) = nested;
        var (discardA, _) = (10, 20);
        return first + second + discardA;
    }

    // Positional pattern connected to same Deconstruct protocol
    public static bool PositionalPattern(Deconstructable item) => item is (10, 20);

    public static bool PositionalPatternThree(Deconstructable item) => item is (10, 20, "stock");

    // Overload by arity selection
    public static string ArityOverload()
    {
        var item = new Deconstructable(1, 2, "x");
        var (a, b) = item;
        var (c, d, e) = item;
        return $"{a}{b}{c}{d}{e}";
    }

    // Ambiguous same-arity candidates is a diagnostic:
    //   var amb = new AmbiguousArity();
    //   var (x) = amb; // CS0121 ambiguous between instance Deconstruct(out int) and extension if both existed with same arity and parameter types
}

public sealed record NestedPair(int Left, int Right)
{
    public void Deconstruct(out int left, out int right)
    {
        left = Left;
        right = Right;
    }
}
