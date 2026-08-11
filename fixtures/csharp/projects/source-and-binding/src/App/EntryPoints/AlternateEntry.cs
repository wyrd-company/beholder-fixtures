using System.Threading.Tasks;

namespace SourceBinding.App.Entry;

public sealed class AlternateEntry
{
    // Alternate candidate, not selected by StartupObject. Demonstrates async Main signature.
    public static async Task<int> Main(string[] args)
    {
        await Task.Delay(1);
        _ = args;
        return 0;
    }
}
