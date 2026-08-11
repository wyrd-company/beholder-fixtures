using System.Diagnostics.CodeAnalysis;

namespace Bakery.TypesAndValues.CSharp12;

// CS-CAN-021: primary constructors — class and struct primary constructors with
// parameters in initializers, methods, base arguments, shadowing; contrast with records.

public class BakeryItem(string name, int batch)
{
    public string Name => name;

    public int Batch => batch;

    private readonly List<string> _tags = new() { name };

    public string Describe() => $"{name}:{batch}";

    public string GetTag(int index) => _tags[index];

    public int BatchPlus(int delta) => batch + delta;

    // Shadowing: parameter 'name' shadows member-like naming; lookup prefers parameter
    public string Shadow(string name) => name.ToUpperInvariant();

    // Captured storage: 'name' and 'batch' are captured; elided if unused elsewhere.
    // Double-storage warning would occur if we also declared a property with same initializer
    // but we avoid it here; comment shows the pattern.
    // public string NameProp { get; } = name; // double-storage if also capturing 'name'
}

public abstract class BakedBase(string category)
{
    public string Category => category;
}

public sealed class BreadItem(string name, int batch, string flour) : BakedBase("bread")
{
    public string Flour => flour;

    public string Describe() => $"{name}:{batch}:{flour}:{Category}";

    // Parameter used in base argument: category is fixed, but could be parameter-driven
    // like : base(categoryParam) would show parameter in base initializer.
}

public sealed class BreadWithBaseParam(string name, string category) : BakedBase(category)
{
    public string Name => name;
}

public struct CrumbStruct(int weight, string tag)
{
    public int Weight => weight;

    public string Tag => tag;

    public CrumbStruct(int weight, string tag, int extra) : this(weight, tag)
    {
        Extra = extra;
    }

    public int Extra { get; }

    public void Deconstruct(out int w, out string t)
    {
        w = weight;
        t = tag;
    }

    public int Add(int delta) => weight + delta;

    // Shadowing inside struct
    public string Shadow(string tag) => tag.ToUpperInvariant();

    // Definite assignment: all fields must be considered assigned before 'this' use
    public static CrumbStruct CreateDefault() => new(0, "plain");
}

// Contrast with record primary constructor: record already has synthesized properties
public record RecordItem(string Name, int Batch);

public sealed record WrapperWithAttributes(
    [property: Obsolete("use Name")]
    string Name,
    int Batch)
{
    // Attribute on primary-constructor parameter with property target demonstrates
    // parameter/property attribute placement specific to primary constructors (record property).
    public string Describe() => $"{Name}:{Batch}";
}

public static class PrimaryConstructorExercises
{
    public static BakeryItem CreateItem() => new("sourdough", 3);

    public static BreadItem CreateBread() => new("rye", 2, "wholemeal");

    public static BreadWithBaseParam CreateWithCategory() => new("baguette", "viennoiserie");

    public static CrumbStruct CreateCrumb() => new(7, "seed");

    public static CrumbStruct CreateCrumbWithExtra() => new(7, "seed", 3);

    public static void ExerciseCapturedVsElided()
    {
        // 'batch' used in Batch property and method => captured storage.
        // If a parameter were only used to initialize a property and never again,
        // the compiler may elide separate storage and use the property backing field.
        BakeryItem item = new("brioche", 5);
        _ = item.BatchPlus(1);
        _ = item.Shadow("test");
    }

    public static void ExerciseShadowing()
    {
        BakeryItem item = new("plain", 1);
        string shadowed = item.Shadow("local");
        _ = shadowed == "LOCAL";

        CrumbStruct crumb = new(2, "tag");
        string shadowedTag = crumb.Shadow("local");
        _ = shadowedTag == "LOCAL";
    }

    public static void ConstructorChaining()
    {
        CrumbStruct fromPrimary = new(4, "a");
        CrumbStruct fromChained = new(4, "a", 9);
        _ = fromChained.Extra == 9 && fromChained.Weight == 4;
        _ = fromPrimary.Tag == "a";
    }

    public static void DefiniteAssignment()
    {
        CrumbStruct crumb = new(5, "seed");
        var (w, t) = crumb;
        _ = w == 5 && t == "seed";
    }

    public static void ContrastWithRecord()
    {
        RecordItem record = new("rye", 4);
        BakeryItem item = new("rye", 4);
        _ = record.Name == item.Name && record.Batch == item.Batch;
    }

    public static void AttributeTarget()
    {
        WrapperWithAttributes wrapper = new("test", 1);
        _ = wrapper.Name;
    }
}
