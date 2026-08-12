namespace Catalog.FunctionsAndAsync.EntryPointTask;

// OutputType=Exe with a single Main candidate makes this async Task Main the
// compiler-selected program entry point, not merely a library method.
public static class AsyncEntryPointHost
{
    public static async Task Main(string[] args)
    {
        await Task.Delay(1);
        Console.WriteLine(args.Length);
    }
}
