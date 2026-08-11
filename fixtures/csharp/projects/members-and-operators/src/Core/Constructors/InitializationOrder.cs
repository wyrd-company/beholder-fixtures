namespace Catalog.Core.Constructors;

public class InitializationOrder
{
    private readonly string _name;
    private readonly int _sequence;

    public int Sequence => _sequence;

    public InitializationOrder()
        : this("default")
    {
    }

    public InitializationOrder(string name)
        : this(name, CreateSequence(name))
    {
    }

    private InitializationOrder(string name, int sequence)
    {
        _name = name;
        _sequence = sequence;
    }

    private static int CreateSequence(string name) => name.Length;
}

public class ChainedInitialization : InitializationOrder
{
    public ChainedInitialization()
        : base("derived")
    {
    }

    public ChainedInitialization(int seed)
        : this()
    {
        Seed = seed;
    }

    public int Seed { get; }
}

public static class StaticInitializationHost
{
    public static readonly int TableSize = CreateSize();

    static StaticInitializationHost()
    {
        TableSize = TableSize + 1;
    }

    private static int CreateSize() => 8;
}

public sealed class FinalizableResource
{
    private bool _released;

    public FinalizableResource() => _released = false;

    ~FinalizableResource()
    {
        _released = true;
    }

    public bool Released => _released;
}

public readonly record struct Coordinate(int X, int Y)
{
    public Coordinate(Coordinate other)
        : this(other.X, other.Y)
    {
    }
}

public struct ExplicitStruct
{
    public int Value;

    public ExplicitStruct(int value)
    {
        Value = value;
    }

    public static ExplicitStruct Create(int value) => new(value);
}

public sealed class VirtualFromBaseConstructor : BaseWithVirtual
{
    public VirtualFromBaseConstructor()
    {
        DispatchDuringConstruction();
    }
}

public class BaseWithVirtual
{
    protected virtual string Name => "base";

    protected void DispatchDuringConstruction() => _ = Name;
}

public sealed class CircularStaticA
{
    public static readonly int Value = CircularStaticB.Offset + 1;

    public static int BaseSeed => 2;
}

public sealed class CircularStaticB
{
    public static readonly int Offset = CircularStaticA.BaseSeed;

    public static int BaseSeed => 2;
}
