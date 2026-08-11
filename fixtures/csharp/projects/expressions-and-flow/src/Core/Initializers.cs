namespace ExpressionsFlow.Core;

using System.Diagnostics.CodeAnalysis;

public sealed class CatalogEntry
{
    public required string Label { get; init; }

    public int Count { get; init; }

    public CatalogEntry Nested { get; set; } = null!;

    public List<string> Tags { get; } = new();

    public Dictionary<string, int> Scores { get; } = new();

    public CatalogEntry()
    {
    }

    [SetsRequiredMembers]
    public CatalogEntry(string label)
    {
        Label = label;
    }
}

public sealed class AddCollection : System.Collections.Generic.IEnumerable<int>
{
    private readonly List<int> _items = new();

    public void Add(int item) => _items.Add(item);

    public void Add(int a, int b)
    {
        _items.Add(a);
        _items.Add(b);
    }

    public IReadOnlyList<int> Items => _items;

    public System.Collections.Generic.IEnumerator<int> GetEnumerator() => _items.GetEnumerator();

    System.Collections.IEnumerator System.Collections.IEnumerable.GetEnumerator() => GetEnumerator();
}

public static class CollectionExtensions
{
    public static void Add(this AddCollection collection, string text)
    {
        collection.Add(int.Parse(text));
    }
}

public sealed class DictionaryHost
{
    public Dictionary<string, int> Map { get; } = new();
}

public record InventoryRecord(string Label, int Count)
{
    public List<string> Tags { get; init; } = new();
}

public record struct PointRecord(int X, int Y);

public static class Initializers
{
    // Object initializer with required/init members, constructor-before-initializer order
    public static CatalogEntry ObjectInitializer()
    {
        var entry = new CatalogEntry { Label = "stock", Count = 3 };
        return entry;
    }

    // Nested member initialization mutates existing member rather than replacing
    public static CatalogEntry NestedInitializer()
    {
        var entry = new CatalogEntry { Label = "root" };
        entry.Nested = new CatalogEntry { Label = "child" };
        var container = new CatalogEntry { Label = "parent" };
        container.Tags.Add("alpha");
        var nestedCollectionInit = new CatalogEntry
        {
            Label = "outer",
            Nested = new CatalogEntry { Label = "inner", Count = 2 },
        };
        _ = container;
        _ = nestedCollectionInit;
        return entry;
    }

    // Alternative valid nested initializer where Nested is initialized before nested member init
    public static CatalogEntry NestedMemberInitializer()
    {
        return new CatalogEntry
        {
            Label = "outer",
            Nested = new CatalogEntry { Label = "inner", Count = 2 },
        };
    }

    // Collection initializer with Add overloads including extension Add
    public static AddCollection CollectionInitializer()
    {
        return new AddCollection { 1, 2, 3, "4" };
    }

    public static AddCollection MixedAddShapes()
    {
        // Uses Add(int), Add(int,int) is not reachable from collection initializer syntax,
        // but Add via extension with string is demonstrated above.
        return new AddCollection { 10, 20 };
    }

    // Dictionary index setters
    public static Dictionary<string, int> DictionaryInitializer()
    {
        return new Dictionary<string, int>
        {
            ["alpha"] = 1,
            ["beta"] = 2,
        };
    }

    // Index initializer with implicit index (C# 13) is also demonstrated in the dedicated context,
    // but the latest LangVersion build already supports it here.
    public static Dictionary<string, int> DictionaryWithIndexOperator()
    {
        var dict = new Dictionary<string, int>();
        dict["gamma"] = 3;
        dict["delta"] = 4;
        // Index initializer syntax:
        return new Dictionary<string, int>
        {
            ["epsilon"] = 5,
            ["zeta"] = 6,
        };
    }

    public static Dictionary<string, int> ImplicitIndexInitializer()
    {
        return new Dictionary<string, int>
        {
            ["a"] = 1,
            ["b"] = 2,
            ["c"] = 3,
        };
    }

    // Record and struct with
    public static InventoryRecord WithRecord()
    {
        var original = new InventoryRecord("stock", 5) { Tags = new List<string> { "a" } };
        return original with { Count = 10 };
    }

    public static PointRecord WithStruct()
    {
        var p = new PointRecord(1, 2);
        return p with { Y = 20 };
    }

    // Constructor-before-initializer order: constructor runs, then initializer assignments.
    public static CatalogEntry ConstructorBeforeInitializer()
    {
        return new CatalogEntry("ctor-label") { Count = 99 };
    }

    // Partial object after exception: if initializer throws, object may be partially initialized.
    public static CatalogEntry? PartialAfterException()
    {
        try
        {
            return new CatalogEntry { Label = ThrowingLabel() };
        }
        catch (InvalidOperationException)
        {
            return null;
        }
    }

    private static string ThrowingLabel() => throw new InvalidOperationException("init failure");

    // Index-from-end ^n in initializer context
    public static int IndexFromEndInInitializer()
    {
        var items = new List<int> { 10, 20, 30, 40 };
        items[^1] = 99;
        return items[^1];
    }

    // Readonly/init failures and invalid anonymous with are diagnostics, shown as comments:
    //   var ro = new { X = 1 } with { X = 2 }; // CS0572 with not valid on anonymous type
    //   entry.Label = "new"; // CS8852 init-only setter can only be assigned in initializer
}

public static class InitializerExercises
{
    public static int Run()
    {
        var a = Initializers.ObjectInitializer();
        var b = Initializers.NestedMemberInitializer();
        var c = Initializers.CollectionInitializer();
        var d = Initializers.DictionaryInitializer();
        var e = Initializers.WithRecord();
        var f = Initializers.WithStruct();
        var g = Initializers.ConstructorBeforeInitializer();
        var h = Initializers.IndexFromEndInInitializer();
        return a.Count + b.Count + c.Items.Count + d.Count + e.Count + f.Y + g.Count + h;
    }
}
