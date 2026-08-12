namespace Catalog.FunctionsAndAsync.Async;

public static class AsyncEntryPointHost
{
    public static async Task Main(string[] args)
    {
        await Task.Delay(1);
        Console.WriteLine(args.Length);
    }
}

public static class AsyncEntryPointWithResultHost
{
    public static async Task<int> Main(string[] args)
    {
        await Task.Delay(1);
        return args.Length;
    }
}
