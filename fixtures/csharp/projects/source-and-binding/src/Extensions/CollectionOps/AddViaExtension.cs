using System.Collections;
using System.Collections.Generic;

namespace SourceBinding.Extensions.CollectionOps;

// Receiver implements IEnumerable but declares no instance Add. It is a valid
// collection-initializer target only because an extension Add is in scope.
public sealed class ExtensibleBag : IEnumerable<int>
{
    private readonly List<int> _items = new();

    public IEnumerator<int> GetEnumerator() => _items.GetEnumerator();

    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

    internal void Store(int value) => _items.Add(value);
}

public static class ExtensibleBagExtensions
{
    // Extension named Add. With no instance Add on ExtensibleBag, both the
    // collection-initializer element binding and a direct receiver.Add(...) call
    // resolve to this extension.
    public static void Add(this ExtensibleBag bag, int value) => bag.Store(value);
}
