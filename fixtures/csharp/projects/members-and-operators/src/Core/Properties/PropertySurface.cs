namespace Catalog.Core.Properties;

public class PropertySurface
{
    private int _count;
    private string _label = "item";

    public virtual int Count
    {
        get => _count;
        set => _count = value;
    }

    public string Label
    {
        get => _label;
        protected set => _label = value;
    }

    public int Doubled => _count * 2;

    public int this[int index]
    {
        get => _count + index;
        set => _count = value - index;
    }

    public int this[string key, int offset]
    {
        get => key.Length + offset;
        set => _count = value;
    }

    public ref int CountRef => ref _count;
}

public class DerivedPropertySurface : PropertySurface
{
    public override int Count
    {
        get => base.Count;
        set => base.Count = value + 1;
    }

    public new int this[int index] => base[index] + 2;
}

public interface IReadable
{
    int ReadableValue { get; }
}

public sealed class ExplicitPropertySurface : IReadable
{
    private int _value;

    int IReadable.ReadableValue => _value + 1;

    public int Value
    {
        get => _value;
        set => _value = value;
    }
}

public sealed class AccessorAttributedProperty
{
    private int _value;

    public int ImplementedValue
    {
        [System.Runtime.CompilerServices.MethodImpl(
            System.Runtime.CompilerServices.MethodImplOptions.AggressiveInlining)]
        get => _value;

        [System.Runtime.CompilerServices.MethodImpl(
            System.Runtime.CompilerServices.MethodImplOptions.AggressiveInlining)]
        set => _value = value;
    }
}

public sealed class RenamedIndexerMetadata
{
    [System.Runtime.CompilerServices.IndexerName("ShelfEntry")]
    public int this[int shelf, int slot] => shelf + slot;
}
