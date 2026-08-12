namespace Catalog.FunctionsAndAsync.EntryPointTaskOfInt;

// OutputType=Exe with a single Main candidate makes this async Task<int> Main the
// compiler-selected program entry point, not merely a library method.
public static class AsyncEntryPointWithResultHost
{
    public static async Task<int> Main(string[] args)
    {
        await Task.Delay(1);
        return args.Length;
    }
}
