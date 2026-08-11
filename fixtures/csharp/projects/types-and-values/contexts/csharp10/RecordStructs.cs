namespace Bakery.TypesAndValues.CSharp10;

// CS-CAN-020: record structs — C# 10 version-gated, with positional/nominal,
// readonly, with, deconstruction, equality, and synthesis suppression.
// CS-CAN-031: parameterless struct construction — C# 10.

public record struct PastryStruct(string Name, int Layers);

public readonly record struct ReadOnlyPastryStruct(string Name, int Layers);

public record struct NominalPastryStruct
{
    public string Name { get; init; }

    public int Layers { get; init; }

    public NominalPastryStruct(string name, int layers)
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

public record struct WithMutableList(List<string> Tags, string Name);

public record struct SuppressedPastryStruct(string Label, int Count)
{
    public bool Equals(SuppressedPastryStruct other) => Label == other.Label;

    public override int GetHashCode() => Label.GetHashCode();
}

public static class RecordStructExercises
{
    public static PastryStruct Create() => new("sourdough", 6);

    public static ReadOnlyPastryStruct CreateReadOnly() => new("rye", 4);

    public static PastryStruct CopyWith(PastryStruct source, string newName) =>
        source with { Name = newName };

    public static bool EqualityByValue(PastryStruct left, PastryStruct right) => left == right;

    public static bool EqualityContractIsValueBased()
    {
        PastryStruct left = new("a", 1);
        PastryStruct right = new("a", 1);
        PastryStruct different = new("a", 2);
        return left == right && left != different;
    }

    public static (string Name, int Layers) DeconstructPositional(PastryStruct s)
    {
        var (name, layers) = s;
        return (name, layers);
    }

    public static (string Name, int Layers) DeconstructNominal(NominalPastryStruct s)
    {
        var (name, layers) = s;
        return (name, layers);
    }

    public static void MutableStructSharing()
    {
        WithMutableList holder = new(new List<string> { "a" }, "holder");
        WithMutableList copy = holder with { Name = "copy" };
        bool sameList = ReferenceEquals(holder.Tags, copy.Tags);
        copy.Tags.Add("b");
        _ = sameList && holder.Tags.Count == 2;
    }

    public static string Print(PastryStruct s) => s.ToString();

    public static PastryStruct MutateViaWith() => new PastryStruct("plain", 2) with { Layers = 5 };
}

// CS-CAN-031: parameterless struct construction — C# 10 explicit parameterless constructors
// and field initializers.

public struct CounterWithParameterless
{
    public int Count = 7;

    public string Label = "starter";

    public CounterWithParameterless()
    {
        Count = 7;
        Label = "starter";
    }

    public CounterWithParameterless(int count)
    {
        Count = count;
        Label = "batch";
    }
}

public struct ChainedCounter
{
    public int Value;

    public string Label;

    public ChainedCounter()
        : this(3, "default")
    {
    }

    public ChainedCounter(int value, string label)
    {
        Value = value;
        Label = label;
    }
}

public static class ParameterlessExercises
{
    public static CounterWithParameterless NewViaParameterless() => new();

    public static CounterWithParameterless DefaultWithoutConstructor() => default;

    public static bool NewVsDefault()
    {
        CounterWithParameterless withNew = new();
        CounterWithParameterless withDefault = default;
        return withNew.Count == 7 && withDefault.Count == 0 && withDefault.Label is null;
    }

    public static ChainedCounter Chained() => new();

    public static T GenericNew<T>() where T : new() => new T();

    public static CounterWithParameterless ViaGeneric() => GenericNew<CounterWithParameterless>();
}
