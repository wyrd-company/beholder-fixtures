namespace Catalog.Core.Fields;

public sealed partial class PartialInitializer
{
    public readonly int Second = CreateSecond();

    private static int CreateSecond() => 2;
}
