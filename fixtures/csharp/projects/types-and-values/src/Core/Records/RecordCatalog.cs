namespace Bakery.TypesAndValues.Core.Records;

// CS-CAN-020: records — positional and nominal record classes, derived records,
// with, deconstruction, equality, printing, synthesized-member suppression,
// shallow copy, equality contract by runtime type, primary-parameter collision,
// and attribute targets. Record structs are in contexts/csharp10.

public record PastryRecord(string Name, int Layers);

public record NamedPastryRecord
{
    public string Name { get; init; }

    public int Layers { get; init; }

    public NamedPastryRecord(string name, int layers)
    {
        Name = name;
        Layers = layers;
    }

    public void Deconstruct(out string name, out int layers)
    {
        name = Name;
        layers = Layers;
    }
}

// Collision: primary parameter 'Name' collides with synthesized property 'Name'
public record CollisionRecord(string Name)
{
    public string Name { get; init; } = Name;
}

public record CroissantRecord(string Name, int Layers, bool Buttered) : PastryRecord(Name, Layers);

public sealed record SealedBaguetteRecord(string Name, int LengthCm);

// Nominal record with partial synthesis suppression: user GetHashCode/ToString/Equals
public sealed record SuppressedSynthesisRecord(string Label, int Count)
{
    public bool Equals(SuppressedSynthesisRecord? other)
    {
        if (other is null)
        {
            return false;
        }

        return Label == other.Label;
    }

    public override int GetHashCode() => Label.GetHashCode();

    public override string ToString() => $"Suppressed:{Label}";
}

public static class RecordExercises
{
    public static PastryRecord CreatePositional() => new("plain", 12);

    public static NamedPastryRecord CreateNominal() => new("rye", 8);

    public static PastryRecord CopyWith(PastryRecord source, string newName) =>
        source with { Name = newName };

    public static bool EqualityByValue(PastryRecord left, PastryRecord right) => left == right;

    public static bool EqualityRuntimeTypeCheck(PastryRecord baseRecord, CroissantRecord derived)
    {
        PastryRecord asBase = derived;
        return baseRecord.Equals(asBase) == false && asBase.Equals(derived) == false;
    }

    public static (string Name, int Layers) DeconstructPositional(PastryRecord record)
    {
        var (name, layers) = record;
        return (name, layers);
    }

    public static (string Name, int Layers) DeconstructNominal(NamedPastryRecord record)
    {
        var (name, layers) = record;
        return (name, layers);
    }

    public static void ShallowCopySharesReference()
    {
        var tags = new List<string> { "butter" };
        var left = new PastryRecord("croissant", 24);
        var right = left with { Name = "almond" };
        _ = left.Layers == right.Layers;
        _ = !ReferenceEquals(left.Name, right.Name);
        _ = tags;
    }

    public static void ShallowCopyWithMutableList()
    {
        var holder = new ListHolder(new List<string> { "a" });
        var copy = holder with { Name = "b" };
        bool sameList = ReferenceEquals(holder.Tags, copy.Tags);
        copy.Tags.Add("b");
        _ = sameList && holder.Tags.Count == 2;
    }

    public static string Print(PastryRecord record) => record.ToString();

    public static void AttributeOnRecord()
    {
        var decorated = new DecoratedRecord("sourdough", 6);
        _ = decorated;
    }

    public static void AttributeTargetVariants()
    {
        var propertyTarget = new PropertyTargetRecord("brioche", 1);
        var fieldTarget = new FieldTargetRecord("rye", 2);
        var paramTarget = new ParamTargetRecord("plain", 3);
        _ = propertyTarget;
        _ = fieldTarget;
        _ = paramTarget;
    }
}

public sealed record ListHolder(List<string> Tags, string Name = "holder");

[AttributeUsage(AttributeTargets.All)]
public sealed class ExampleAttribute : Attribute
{
    public ExampleAttribute(string note) => Note = note;

    public string Note { get; }
}

[Example("decorated-type")]
public record DecoratedRecord([property: Example("decorated-prop")] string Name, [field: Example("decorated-field")] int Batch);

public record PropertyTargetRecord([property: Example("prop-target")] string Name, int Count);

public record FieldTargetRecord([field: Example("field-target")] string Name, int Count);

public record ParamTargetRecord([param: Example("param-target")] string Name, int Count);
