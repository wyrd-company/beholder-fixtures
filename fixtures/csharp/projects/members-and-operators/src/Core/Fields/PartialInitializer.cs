namespace Catalog.Core.Fields;

public sealed partial class PartialInitializer
{
    public readonly int First = CreateFirst();

    private static int CreateFirst() => 1;
}
