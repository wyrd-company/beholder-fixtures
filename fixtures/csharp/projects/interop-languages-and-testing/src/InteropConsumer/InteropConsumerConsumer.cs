// Additional consumer surface for indexer/default-member and static shapes
using Acme.InteropProducer;

namespace Acme.InteropConsumer;

public sealed class ContainerHolder
{
    private readonly Container _container;

    public ContainerHolder(int capacity)
    {
        _container = new Container(capacity);
    }

    public int Capacity => _container.Capacity;

    // Default-member indexer forwarded through holder
    public int this[int index]
    {
        get => _container[index];
        set => _container[index] = value;
    }
}
