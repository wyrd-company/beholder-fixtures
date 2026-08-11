namespace Bakery.TypesAndValues.Core.Boxing;

// CS-CAN-058: boxing, unboxing, constrained value-type dispatch —
// box mutable struct to object/interface, mutate original and boxed copies,
// constrained generic calls, nullable/enum boxing, explicit-interface, readonly defensive copy.

public interface IStamp
{
    int Mark { get; }

    void Stamp(int value);

    string Describe();
}

public struct MutableCounter : IStamp
{
    public int Mark { get; private set; }

    public MutableCounter(int mark) => Mark = mark;

    public void Stamp(int value) => Mark = value;

    public string Describe() => $"mark:{Mark}";

    public override string ToString() => Describe();
}

public struct ExplicitStamp : IStamp
{
    private int _mark;

    public int Mark => _mark;

    void IStamp.Stamp(int value) => _mark = value;

    public string Describe() => $"explicit:{_mark}";
}

public readonly struct ReadOnlyStamp : IStamp
{
    private readonly int _mark;

    public ReadOnlyStamp(int mark) => _mark = mark;

    public int Mark => _mark;

    public void Stamp(int value)
    {
        // Mutable method on readonly struct — calling via readonly receiver copies.
        ReadOnlyStamp copy = this;
        _ = copy;
        _ = value;
    }

    public string Describe() => $"readonly:{_mark}";
}

public static class BoxingExercises
{
    public static void BoxMutableStruct()
    {
        MutableCounter counter = new(3);
        object boxed = counter;
        counter.Stamp(10);
        bool originalMutated = counter.Mark == 10;
        bool boxedUnchanged = ((MutableCounter)boxed).Mark == 3;
        _ = originalMutated && boxedUnchanged;
    }

    public static void BoxToInterfaceAndMutate()
    {
        MutableCounter counter = new(4);
        IStamp boxedInterface = counter;
        counter.Stamp(9);
        bool interfaceSeesOriginalBox = boxedInterface.Mark == 4;
        boxedInterface.Stamp(11);
        bool interfaceCopyMutated = boxedInterface.Mark == 11 && counter.Mark == 9;
        _ = interfaceSeesOriginalBox && interfaceCopyMutated;
    }

    public static void ExplicitInterfaceBoxing()
    {
        ExplicitStamp stamp = new();
        IStamp iface = stamp;
        iface.Stamp(7);
        _ = iface.Mark == 7 && stamp.Mark == 0;
    }

    public static void ReturnViaInterface(MutableCounter counter)
    {
        IStamp iface = counter;
        _ = iface.Describe();
    }

    public static void ConstrainedGenericCall<T>(ref T stamp, int value) where T : struct, IStamp
    {
        stamp.Stamp(value);
        _ = stamp.Mark;
    }

    public static void ConstrainedVsBoxed()
    {
        MutableCounter counter = new(1);
        ConstrainedGenericCall(ref counter, 12);
        bool viaConstrainedMutatedInPlace = counter.Mark == 12;

        MutableCounter second = new(2);
        IStamp boxed = second;
        boxed.Stamp(20);
        bool boxedDidNotMutateOriginal = second.Mark == 2 && boxed.Mark == 20;
        _ = viaConstrainedMutatedInPlace && boxedDidNotMutateOriginal;
    }

    public static void ReadOnlyDefensiveCopy()
    {
        ReadOnlyStamp stamp = new(5);
        stamp.Stamp(99);
        bool unchanged = stamp.Mark == 5;
        _ = unchanged;

        var holder = new ReadOnlyHolder();
        holder.Exercise();
    }

    public static void NullableBoxing()
    {
        int? present = 7;
        int? absent = null;
        object? boxedPresent = present;
        object? boxedAbsent = absent;
        bool presentIsInt = boxedPresent is int i && i == 7;
        bool absentIsNull = boxedAbsent is null;
        _ = presentIsInt && absentIsNull;

        int? roundTrip = (int?)boxedPresent;
        _ = roundTrip == 7;
    }

    public static void EnumBoxing()
    {
        BakeEnum value = BakeEnum.Sourdough;
        object boxed = value;
        BakeEnum unboxed = (BakeEnum)boxed;
        bool equal = value == unboxed;
        _ = equal;

        IComparable comparable = value;
        _ = comparable.CompareTo(BakeEnum.Sourdough) == 0;
    }

    public static void InvalidUnbox()
    {
        object boxedInt = 42;
        try
        {
            long bad = (long)boxedInt;
            _ = bad;
        }
        catch (InvalidCastException)
        {
            _ = true;
        }

        try
        {
            BakeEnum wrong = (BakeEnum)boxedInt;
            _ = wrong;
        }
        catch (InvalidCastException)
        {
            _ = true;
        }
    }

    public static void IdentityComparison()
    {
        MutableCounter counter = new(3);
        object first = counter;
        object second = counter;
        bool differentReferences = !ReferenceEquals(first, second);
        bool equalValue = first.Equals(second);
        _ = differentReferences && equalValue;
    }

    public static void OverriddenVsInheritedObjectMethod()
    {
        MutableCounter counter = new(4);
        object boxed = counter;
        string overridden = boxed.ToString()!;
        _ = overridden == "mark:4";

        ExplicitStamp explicitStamp = new();
        object boxedExplicit = explicitStamp;
        string inherited = boxedExplicit.ToString()!;
        _ = inherited is not null;
    }

    private sealed class ReadOnlyHolder
    {
        public readonly ReadOnlyStamp Field = new(6);

        public void Exercise()
        {
            Field.Stamp(99);
            _ = Field.Mark == 6;
        }
    }

    private enum BakeEnum
    {
        Plain = 0,
        Sourdough = 1,
        Rye = 2,
    }
}
