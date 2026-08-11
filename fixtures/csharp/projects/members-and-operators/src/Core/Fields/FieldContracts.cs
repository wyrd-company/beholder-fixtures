namespace Catalog.Core.Fields;

public static class SharedLimits
{
    public const int DefaultCapacity = 16;
    public const string DefaultLabel = "stock";
}

public sealed class FieldContracts
{
    public const int TableWidth = 4;

    public static readonly DateOnly Epoch = new(2020, 1, 1);

    public readonly int InstanceSeed = 7;

    public volatile int RefreshCount;

    public static int SharedCounter;

    public int MutableCount;

    static FieldContracts()
    {
        SharedCounter = TableWidth;
    }

    public FieldContracts(int seed)
    {
        InstanceSeed = seed;
        MutableCount = seed;
    }
}

public sealed class CircularPartnerA
{
    public static readonly int PartnerValue = CircularPartnerB.PartnerValue + 1;
}

public sealed class CircularPartnerB
{
    public static readonly int PartnerValue = SharedLimits.DefaultCapacity + 2;
}

public static class BeforeFieldInitContrast
{
    public static int EagerValue = CreateEager();

    private static int CreateEager() => 3;
}

public sealed class BeforeFieldInitHolder
{
    public static int LazyValue = CreateLazy();

    private static int CreateLazy() => 5;
}

static class BeforeFieldInitHolderStatic
{
    static BeforeFieldInitHolderStatic()
    {
        _ = BeforeFieldInitHolder.LazyValue;
    }
}
