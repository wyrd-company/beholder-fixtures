namespace ExpressionsFlow.CSharp13;

public sealed class IndexHost
{
    public List<int> Items { get; } = new() { 10, 20, 30, 40 };
}

public static class ImplicitIndex
{
    // C# 13 implicit index access inside object initializer: nested member initializer with index-from-end
    public static IndexHost HostWithImplicitIndex()
    {
        return new IndexHost { Items = { [^1] = 99, [^2] = 88 } };
    }

    public static IndexHost HostSingle()
    {
        return new IndexHost { Items = { [^1] = 42 } };
    }

    public static int ReadImplicit()
    {
        var host = HostWithImplicitIndex();
        return host.Items[^1];
    }
}
