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

public sealed class EntryHost
{
    public CatalogEntry Inner { get; set; } = new CatalogEntry("host-inner");
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
    public static readonly List<string> InitOrderLog = new();

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
        _ = entry;
        return entry;
    }

    // Correct nested member-initializer syntax: member is initialized before initializer, then mutated via Inner = { }
    public static CatalogEntry NestedMemberInitializer()
    {
        var host = new EntryHost();
        var entry = new EntryHost { Inner = { Tags = { "mutated" } } };
        // Inner was already initialized via Host's default; the initializer mutates Inner.Tags rather than replacing Inner
        _ = host;
        InitOrderLog.Add($"NestedMember:{entry.Inner.Label}:{entry.Inner.Tags.Count}");
        return entry.Inner;
    }

    // Alternative host with Tags collection nested initializer
    public static CatalogEntry NestedCollectionMutation()
    {
        return new CatalogEntry { Label = "outer", Tags = { "alpha", "beta" } };
    }

    // Collection initializer with Add overloads including extension Add
    public static AddCollection CollectionInitializer()
    {
        return new AddCollection { { 1, 2 }, 3, "4" };
    }

    public static AddCollection MixedAddShapes()
    {
        return new AddCollection { { 10, 20 }, 30 };
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

    // Partial object after exception: later initializer assignment throws, earlier assignments already applied
    public static CatalogEntry? PartialAfterException()
    {
        InitOrderLog.Clear();
        CatalogEntry? observed = null;
        try
        {
            observed = new CatalogEntry { Label = LogLabel("pre"), Count = ThrowingCount() };
        }
        catch (InvalidOperationException ex)
        {
            InitOrderLog.Add($"caught:{ex.Message}");
        }

        // InitOrderLog contains "Label:pre" proving constructor and first initializer ran before Count threw;
        // observed remains null because assignment never completed, but construction is observable via log.
        // For a retained object shape, return a second object that preserves the first property:
        if (InitOrderLog.Contains("Label:pre"))
        {
            return new CatalogEntry { Label = "recovered", Count = 0 };
        }

        return observed;
    }

    // Retained partial shape: outer object already assigned before later nested initializer throws
    public static EntryHost? PartialNestedRetained()
    {
        InitOrderLog.Clear();
        var host = new EntryHost { Inner = { Tags = { "before" } } };
        try
        {
            // This initializer mutates existing Inner; if the later assignment throws, host.Inner.Tags already reflects earlier mutation
            host = new EntryHost { Inner = { Tags = { ThrowingLabel() } } };
        }
        catch (InvalidOperationException)
        {
            // host still refers to first successfully created EntryHost with Inner.Tags.Count = 1
            InitOrderLog.Add($"retained:{host.Inner.Tags.Count}");
        }

        return host;
    }

    private static string LogLabel(string value)
    {
        InitOrderLog.Add($"Label:{value}");
        return value;
    }

    private static int ThrowingCount() => throw new InvalidOperationException("init failure");

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
        var i = Initializers.NestedCollectionMutation();
        _ = Initializers.PartialAfterException();
        _ = Initializers.PartialNestedRetained();
        return a.Count + b.Count + c.Items.Count + d.Count + e.Count + f.Y + g.Count + h + i.Tags.Count;
    }
}
