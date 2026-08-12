namespace Bakery.TypesAndValues.Core.StructConstruction;

// CS-CAN-031: struct construction, defaults, copies, mutation —
// contrast new S() vs default(S), field initializers, auto-default fields,
// readonly receivers, boxing copies, mutable struct behavior.

public struct Counter
{
    public int Value;

    public Counter(int value) => Value = value;

    public void Increment() => Value++;

    public Counter WithAdded(int delta) => new(Value + delta);
}

public struct MeasuredIngredient
{
    public int Grams;
    public string Label;

    public MeasuredIngredient(int grams, string label)
    {
        Grams = grams;
        Label = label;
    }

    public static MeasuredIngredient Create(int grams) => new(grams, "flour");
}

public struct WithInitializer
{
    public int Count = 3;

    public string Label = "sourdough";

    public WithInitializer()
    {
    }

    public WithInitializer(int count)
    {
        Count = count;
        Label = "rye";
    }
}

public readonly struct ReadOnlyCrumb
{
    public readonly int Weight;
    public readonly string Tag;

    public ReadOnlyCrumb(int weight, string tag)
    {
        Weight = weight;
        Tag = tag;
    }

    public int DescribeLength() => Tag.Length + Weight;
}

public struct MutableStamp
{
    public int Mark;

    public void Stamp(int value) => Mark = value;
}

public sealed class StampHolder
{
    public MutableStamp Field;

    public readonly MutableStamp ReadOnlyField = new() { Mark = 5 };

    public void MutateViaField()
    {
        Field.Stamp(7);
        _ = Field.Mark;
    }

    public void DefensiveCopyViaReadOnly()
    {
        // Calling a mutating method on a readonly field makes a defensive copy;
        // the field itself is not mutated.
        ReadOnlyField.Stamp(99);
        bool unchanged = ReadOnlyField.Mark == 5;
        _ = unchanged;
    }

    public void MutateViaInParameter(in MutableStamp stamp)
    {
        int original = stamp.Mark;
        stamp.Stamp(11);
        bool unchanged = stamp.Mark == original;
        _ = unchanged;
    }
}

public static class StructExercises
{
    public static Counter NewCounter() => new Counter(5);

    public static Counter DefaultCounter() => default;

    public static Counter DefaultLiteral() => default(Counter);

    public static bool NewVsDefault()
    {
        Counter withNew = new Counter();
        Counter withDefault = default;
        return withNew.Value == withDefault.Value && withNew.Value == 0;
    }

    public static bool NewAndDefaultAreEqual(Counter a, Counter b)
    {
        Counter x = new();
        Counter y = default;
        return x.Value == y.Value && a.Value == b.Value;
    }

    public static void CopySemantics()
    {
        Counter left = new(10);
        Counter copy = left;
        copy.Increment();
        bool independent = left.Value == 10 && copy.Value == 11;
        _ = independent;
    }

    public static void BoxingCopy()
    {
        Counter counter = new(7);
        object boxed = counter;
        Counter unboxed = (Counter)boxed;
        unboxed.Increment();
        bool boxedUnchanged = ((Counter)boxed).Value == 7 && unboxed.Value == 8;
        _ = boxedUnchanged;
    }

    public static void MutableStructViaBoxing()
    {
        MutableStamp stamp = new() { Mark = 1 };
        object boxed = stamp;
        ((MutableStamp)boxed).Stamp(9);
        bool stillOriginal = ((MutableStamp)boxed).Mark == 1;
        _ = stillOriginal;

        var boxed2 = (MutableStamp)boxed;
        boxed2.Stamp(9);
        _ = boxed2.Mark == 9;
    }

    public static T GenericNew<T>() where T : new() => new T();

    public static Counter ViaGenericNew() => GenericNew<Counter>();

    public static void ChainedConstruction()
    {
        WithInitializer a = new();
        WithInitializer b = new(10);
        _ = a.Count == 3 && b.Count == 10;
    }

    public static void ReadOnlyReceiver()
    {
        ReadOnlyCrumb crumb = new(4, "seed");
        int length = crumb.DescribeLength();
        _ = length;
    }

    public static void ExerciseHolderCopies()
    {
        StampHolder holder = new();
        holder.MutateViaField();
        holder.DefensiveCopyViaReadOnly();
        MutableStamp stamp = new() { Mark = 2 };
        holder.MutateViaInParameter(in stamp);
        _ = stamp.Mark == 2;
    }
}
