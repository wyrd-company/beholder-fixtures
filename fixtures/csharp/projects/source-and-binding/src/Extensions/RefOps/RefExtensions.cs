namespace SourceBinding.Extensions.RefOps;

public static class RefExtensions
{
    public static void Increment(this ref int value) => value++;

    public static void ReadOnlyView(this in int value, out int copy) => copy = value;
}
